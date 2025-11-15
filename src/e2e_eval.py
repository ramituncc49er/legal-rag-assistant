"""
e2e_eval.py

- Inputs:
    - queries JSONL (same you used for inference; must include at least query_id, query_text, reference_answer,
    and ideally one of: gold_doc_ids OR gold_case_id OR gold_citations)
    - inference_results JSONL produced by inference.py (one JSON object per query; may start with a header row {"_run_info": ...})
    - LanceDB collection (to re-fetch docs for grounding checks)

- Metrics:
    Retrieval:
        * Recall@K, MRR@K (K from the inference 'retrieval.k'; can also compute at standard K=[5,10,20,50])

    Generation:
        * ROUGE-L F1 vs. reference_answer (quick lexical proxy)
        * Length and latency summaries

    Grounding & Citations (heuristic):
        * Citation correctness: numeric cites like [1], [2] must be <= K and refer to retrieved docs
        * Support check: cited doc text shares n-grams with the sentence around that citation

    Faithfulness (heuristic):
        * Overlap ratio between answer tokens and concatenated top-K context
        * Hallucination rate: fraction of CapitalizedTokens in answer not found in context

- Assumptions:
    - retriever.py exposes HybridRetriever(db_dir, collection_name, embed_model_name, ...), with search_hybrid(query, k, alpha, bm25_k, dense_k) -> list[(doc_id, score)], fetch_docs(id_scores) -> list[Document], where Document.page_content and Document.metadata exist
"""

import argparse, json, os, re, statistics, math, itertools
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict, Counter

import sys
sys.path.append(os.path.dirname(__file__))
from retriever import HybridRetriever

# ================== Helpers ==================
def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s: continue
            obj = json.loads(s)
            rows.append(obj)
    return rows

def index_by(rows: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out = {}
    for r in rows:
        if key in r:
            out[r[key]] = r
    return out

def extract_gold_ids(q: Dict[str, Any]) -> Dict[str, Any]:
    """
    We try multiple ways to find gold relevance labels:
      1) q["gold_doc_ids"] -> list of exact doc ids (preferred)
      2) q["gold_case_id"] -> match to doc.metadata["case_id"]
      3) q["gold_citations"] -> match to any of [us_cite, sct_cite, led_cite, lexis_cite] in metadata
    Returns a dict with one of the following keys set:
      {"gold_doc_ids": [...]} or {"gold_case_id": "..."} or {"gold_citations": ["...","..."]}
    """
    if "gold_doc_ids" in q and q["gold_doc_ids"]:
        return {"gold_doc_ids": q["gold_doc_ids"]}
    if "gold_case_id" in q and q["gold_case_id"]:
        return {"gold_case_id": q["gold_case_id"]}
    if "gold_citations" in q and q["gold_citations"]:
        return {"gold_citations": q["gold_citations"]}
    # Fallback: if your queries carry "us_cite" or "case_name"
    for k in ("us_cite","sct_cite","led_cite","lexis_cite"):
        if k in q and q[k]:
            return {"gold_citations": [q[k]]}
    return {}

def doc_matches_gold(doc, gold: Dict[str, Any]) -> bool:
    md = getattr(doc, "metadata", {}) or {}
    if "gold_doc_ids" in gold:
        did = getattr(doc, "id", None) or md.get("id")
        return did in set(gold["gold_doc_ids"])
    if "gold_case_id" in gold:
        return md.get("case_id") == gold["gold_case_id"]
    if "gold_citations" in gold:
        cites = set([str(x).strip() for x in gold["gold_citations"]])
        for k in ("us_cite","sct_cite","led_cite","lexis_cite","citation","cite"):
            v = md.get(k)
            if v and str(v).strip() in cites:
                return True
    return False

_NONWORD = re.compile(r"\W+")
_UPPER_TOKEN = re.compile(r"^[A-Z][A-Za-z0-9\-]+$")  # crude NamedToken proxy

def toks(s: str) -> List[str]:
    return [t for t in _NONWORD.split(s or "") if t]

def sentences(s: str) -> List[str]:
    return re.split(r"(?<=[\.\?\!])\s+", s.strip()) if s else []

def rouge_l_f1(ref: str, hyp: str) -> float:
    # simple LCS-based ROUGE-L F1 (token-level)
    r = toks(ref.lower())
    h = toks(hyp.lower())
    if not r or not h:
        return 0.0
    # LCS DP
    dp = [[0]*(len(h)+1) for _ in range(len(r)+1)]
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    lcs = dp[-1][-1]
    prec = lcs / len(h)
    rec  = lcs / len(r)
    if prec + rec == 0: return 0.0
    return 2*prec*rec/(prec+rec)

# ================== Citation parsing ==================
_CITE_NUM = re.compile(r"\[(?:cite:\s*)?\[?(\d{1,3})\]?\]")  # matches [1], [cite: [2]], etc.

def find_numeric_citations(answer: str) -> List[int]:
    return [int(m.group(1)) for m in _CITE_NUM.finditer(answer or "")]

# ================== Metrics ==================
def recall_at_k(ranks: List[int], K: int) -> float:
    return 1.0 if any(r <= K for r in ranks) else 0.0

def mrr_at_k(ranks: List[int], K: int) -> float:
    valid = [r for r in ranks if r <= K]
    return 1.0/valid[0] if valid else 0.0

# ================== Eval core ==================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries_file", required=True)
    ap.add_argument("--inference_results", required=True)
    ap.add_argument("--db_dir", required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--embed_model", default="jinaai/jina-embeddings-v3")
    ap.add_argument("--recompute_context", action="store_true",
                    help="Re-run retrieval to reconstruct [1..K] ordering (recommended).")
    ap.add_argument("--standard_ks", default="5,10,20,50")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    queries = load_jsonl(args.queries_file)
    infrows = load_jsonl(args.inference_results)

    # Allow header row {"_run_info": ...}
    run_info = None
    if infrows and "_run_info" in infrows[0]:
        run_info = infrows[0]["_run_info"]
        infrows = infrows[1:]

    q_by_id = index_by(queries, "query_id")
    inf_by_id = index_by(infrows, "query_id")

    # retriever for recompute
    retr = HybridRetriever(
        db_dir=args.db_dir,
        collection_name=args.collection,
        embed_model_name=args.embed_model,
        bm25_enabled=True,
        reranker_model=None,
        hf_device="cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
    )

    Ks = [int(x) for x in args.standard_ks.split(",") if x.strip()]
    all_rows = []
    miss_gold = 0

    for qid, inf in inf_by_id.items():
        q = q_by_id.get(qid)
        if not q:
            continue

        qtext = q.get("query_text","")
        ref   = q.get("reference_answer","") or inf.get("reference_answer","")
        gen   = inf.get("generated_answer","")

        # reconstruct retrieval list in the same mode/config
        k_conf = inf.get("retrieval", {}) or {}
        K = int(k_conf.get("k", 50))
        alpha   = float(k_conf.get("alpha", 0.6))
        dense_k = int(k_conf.get("dense_k", 120))
        bm25_k  = int(k_conf.get("bm25_k", 200))

        if args.recompute_context:
            id_scores = retr.search_hybrid(qtext, k=K, alpha=alpha, dense_k=dense_k, bm25_k=bm25_k)
            docs = retr.fetch_docs(id_scores)
            doc_ids_ordered = [cid for cid,_ in id_scores]
        else:
            # trust stored ids; we still fetch to read text for grounding
            pred_ids = inf.get("pred_chunk_ids", [])
            id_scores = [(cid, 0.0) for cid in pred_ids]
            docs = retr.fetch_docs(id_scores)
            doc_ids_ordered = pred_ids

        # Retrieval metrics (needs gold)
        gold = extract_gold_ids(q)
        if not gold:
            miss_gold += 1

        # compute ranks for all docs that match gold
        ranks = []
        for idx, d in enumerate(docs, start=1):
            if doc_matches_gold(d, gold):
                ranks.append(idx)

        ret_metrics = {}
        for S in Ks:
            ret_metrics[f"Recall@{S}"] = recall_at_k(ranks, S) if gold else math.nan
            ret_metrics[f"MRR@{S}"]    = mrr_at_k(ranks, S) if gold else math.nan

        # Generation metrics
        rougeL = rouge_l_f1(ref, gen) if ref else math.nan

        # Grounding/citation correctness
        numeric_cites = find_numeric_citations(gen)
        # valid if in [1..K]
        cite_in_range = [c for c in numeric_cites if 1 <= c <= len(doc_ids_ordered)]
        cite_valid_ratio = (len(cite_in_range) / len(numeric_cites)) if numeric_cites else 1.0

        # Light "support" check: sentence around each cite should share 3+ tokens with cited doc
        support_hits = 0
        ctx_texts = [getattr(d, "page_content", "") or "" for d in docs]
        sents = sentences(gen)
        for s in sents:
            for c in find_numeric_citations(s):
                if 1 <= c <= len(ctx_texts):
                    answer_t = set(toks(s.lower()))
                    doc_t    = set(toks(ctx_texts[c-1].lower()))
                    if len(answer_t & doc_t) >= 3:
                        support_hits += 1
        support_ratio = (support_hits / max(1, len(numeric_cites))) if numeric_cites else math.nan

        # Faithfulness (heuristic)
        ctx_cat = " ".join(ctx_texts[:K])
        a_toks = set(toks(gen.lower()))
        c_toks = set(toks(ctx_cat.lower()))
        overlap = len(a_toks & c_toks) / max(1, len(a_toks))

        # crude hallucination proxy: Capitalized tokens not present in context
        cap_ans = [t for t in toks(gen) if _UPPER_TOKEN.match(t)]
        cap_ctx = set([t for t in toks(ctx_cat)])
        halluc_rate = (len([t for t in cap_ans if t not in cap_ctx]) / max(1, len(cap_ans))) if cap_ans else math.nan

        row = {
            "query_id": qid,
            "model_name": inf.get("model_name",""),
            "K_prompt": K,
            "retrieval_latency_ms": inf.get("retrieval_latency_ms"),
            "generation_latency_ms": inf.get("generation_latency_ms"),
            "rougeL_f1": rougeL,
            "cite_count": len(numeric_cites),
            "cite_valid_ratio": cite_valid_ratio,
            "support_ratio": support_ratio,
            "faithfulness_overlap": overlap,
            "hallucination_rate": halluc_rate,
        }
        row.update(ret_metrics)
        all_rows.append(row)

        if args.verbose:
            print(f"{qid} | RL={rougeL:.3f} | cite_ok={cite_valid_ratio:.2f} | support={support_ratio if not math.isnan(support_ratio) else -1:.2f} | overlap={overlap:.2f}")

    # Aggregate
    def agg_mean(key):
        vals = [r[key] for r in all_rows if isinstance(r[key], (int,float)) and not math.isnan(r[key])]
        return statistics.mean(vals) if vals else math.nan

    summary = {
        "N_evaluated": len(all_rows),
        "N_missing_gold": miss_gold,
        "mean_rougeL_f1": agg_mean("rougeL_f1"),
        "mean_cite_valid_ratio": agg_mean("cite_valid_ratio"),
        "mean_support_ratio": agg_mean("support_ratio"),
        "mean_faithfulness_overlap": agg_mean("faithfulness_overlap"),
        "mean_hallucination_rate": agg_mean("hallucination_rate"),
    }
    # Add retrieval means per K
    for k in args.standard_ks.split(","):
        k = k.strip()
        if not k: continue
        summary[f"mean_Recall@{k}"] = agg_mean(f"Recall@{k}")
        summary[f"mean_MRR@{k}"]    = agg_mean(f"MRR@{k}")

    print("\n===== SUMMARY =====")
    for k,v in summary.items():
        print(f"{k}: {v}")

    # Write per-query CSV + summary JSON next to inference file
    base = os.path.splitext(args.inference_results)[0]
    out_csv = base + ".e2e_eval.csv"
    out_json = base + ".e2e_eval.summary.json"

    cols = sorted(all_rows[0].keys()) if all_rows else []
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write(",".join(cols) + "\n")
        for r in all_rows:
            vals = []
            for c in cols:
                v = r.get(c, "")
                if isinstance(v, float) and math.isnan(v):
                    vals.append("")
                else:
                    s = str(v).replace(",", " ")
                    vals.append(s)
            f.write(",".join(vals) + "\n")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nWrote per-query metrics: {out_csv}")
    print(f"Wrote summary:          {out_json}")

if __name__ == "__main__":
    main()