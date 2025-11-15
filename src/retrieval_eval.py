"""
retrieval_eval.py

Benchmark the retriever:
    - compute recall@k, 
    - compute MRR@k, 
    - compute hit/miss stats 
    - compute latency percentiles.
"""

import argparse, json, math, os, time, hashlib, statistics
from typing import Any, Dict, List
from collections import defaultdict

import sys
sys.path.append(os.path.dirname(__file__))
from retriever import HybridRetriever 

#import mlflow

try:
    import torch
    _CUDA = torch.cuda.is_available()
except Exception:
    _CUDA = False

# ================== Helpers ==================
def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def normalize_strata(row: dict, keys=("type","issueArea","decade")) -> tuple:
    """Return a 3-tuple for strata, tolerating dict / str / list / None."""
    s = row.get("strata", {})
    if isinstance(s, dict):
        return tuple(str(s.get(k, "")) for k in keys)
    if isinstance(s, (list, tuple)):
        vals = [str(x) for x in s]
        vals += [""] * (len(keys) - len(vals))
        return tuple(vals[:len(keys)])
    if isinstance(s, str):
        return (s, "", "") if len(keys) >= 3 else (s,)
    return tuple("" for _ in keys)

# ================== Metrics ==================
def recall_at_k(golds: List[str], preds: List[str], k: int) -> float:
    if not golds:
        return 0.0
    topk = preds[:k]
    return 1.0 if any(pid in topk for pid in golds) else 0.0

def mrr_at_k(golds: List[str], preds: List[str], k: int) -> float:
    for i, pid in enumerate(preds[:k], start=1):
        if pid in golds:
            return 1.0 / i
    return 0.0

def ndcg_at_k(golds: List[str], preds: List[str], k: int) -> float:
    dcg = 0.0
    for i, pid in enumerate(preds[:k], start=1):
        gain = 1.0 if pid in golds else 0.0
        dcg += gain / math.log2(i + 1)
    ideal_hits = min(len(golds), k)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return dcg / idcg if idcg > 0 else 0.0

def p50_p95(values_ms: List[float]) -> (float, float):
    if not values_ms:
        return float("nan"), float("nan")
    p50 = statistics.median(values_ms)
    idx = max(0, int(round(0.95 * (len(values_ms) - 1))))
    p95 = sorted(values_ms)[idx]
    return float(p50), float(p95)

# ================== Eval core ==================
def _get_pred_ids(hr: HybridRetriever, q: str, k: int, mode: str, alpha: float,
                  bm25_k: int|None, dense_k: int|None) -> List[str]:
    """Use your HybridRetriever to get top-k chunk_ids for the query."""
    if mode == "dense":
        pairs = hr.search_dense(q, k=k)
    elif mode == "bm25":
        pairs = hr.search_bm25(q, k=k)
    elif mode == "hybrid":
        pairs = hr.search_hybrid(query=q, k=k, alpha=alpha, bm25_k=bm25_k, dense_k=dense_k)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    # pairs are (chunk_id, score)
    return [cid for cid, _ in pairs[:k]]

def eval_retrieval(args) -> Dict[str, Any]:
    rows = load_jsonl(args.eval_file)
    if args.max_queries and args.max_queries > 0:
        rows = rows[:args.max_queries]

    queries = [r["query_text"] for r in rows]
    golds_list = [list(map(str, r.get("gold_chunk_ids", []))) for r in rows]

    strata_keys = ("type", "issueArea", "decade")
    strata_vals = [normalize_strata(r, strata_keys) for r in rows]

    # Init your retriever (BM25 enabled when needed)
    retr = HybridRetriever(
        db_dir=args.db_dir,
        collection_name=args.collection,
        embed_model_name=args.embed_model,
        bm25_enabled=(args.mode in ["bm25", "hybrid"]),
        reranker_model=None,            # keep off per your request
        hf_device=args.device,
    )

    # Run searches
    lat_ms, rec5, rec10, mrr10, ndcg10 = [], [], [], [], []
    per_query_dump = []
    topk_eval = max(args.k, 10)

    for i, (q, golds) in enumerate(zip(queries, golds_list)):
        t0 = time.time()
        preds = _get_pred_ids(
            retr, q, k=topk_eval, mode=args.mode, alpha=args.alpha,
            bm25_k=args.bm25_k, dense_k=args.dense_k
        )
        lat_ms.append((time.time() - t0) * 1000.0)

        rec5.append(recall_at_k(golds, preds, 5))
        rec10.append(recall_at_k(golds, preds, 10))
        mrr10.append(mrr_at_k(golds, preds, 10))
        ndcg10.append(ndcg_at_k(golds, preds, 10))

        if args.dump_results:
            per_query_dump.append({
                "query_id": rows[i].get("query_id", f"q{i:04d}"),
                "pred_chunk_ids": preds,
                "gold_chunk_ids": golds,
                "latency_ms": lat_ms[-1],
                "strata": rows[i].get("strata", {}),
                "mode": args.mode,
                "alpha": args.alpha if args.mode == "hybrid" else None
            })

    # Aggregate
    p50, p95 = p50_p95(lat_ms)
    metrics = {
        "retrieval/recall@5": float(sum(rec5)/len(rec5)) if rec5 else float("nan"),
        "retrieval/recall@10": float(sum(rec10)/len(rec10)) if rec10 else float("nan"),
        "retrieval/mrr@10": float(sum(mrr10)/len(mrr10)) if mrr10 else float("nan"),
        "retrieval/ndcg@10": float(sum(ndcg10)/len(ndcg10)) if ndcg10 else float("nan"),
        "retrieval/p50_ms": p50,
        "retrieval/p95_ms": p95,
        "count": len(rows),
        "mode": args.mode,
        "alpha": args.alpha if args.mode == "hybrid" else None
    }

    # Per-strata breakdowns (optional)
    if args.by_strata:
        buckets = defaultdict(list)
        for i, key in enumerate(strata_vals):
            buckets[key].append(i)
        metrics["by_strata"] = {}
        for key, idxs in buckets.items():
            if not idxs:
                continue
            r5 = sum(rec5[j] for j in idxs) / len(idxs)
            r10 = sum(rec10[j] for j in idxs) / len(idxs)
            mrr = sum(mrr10[j] for j in idxs) / len(idxs)
            ndc = sum(ndcg10[j] for j in idxs) / len(idxs)
            p50_b, p95_b = p50_p95([lat_ms[j] for j in idxs])
            metrics["by_strata"][str(key)] = {
                "retrieval/recall@5": float(r5),
                "retrieval/recall@10": float(r10),
                "retrieval/mrr@10": float(mrr),
                "retrieval/ndcg@10": float(ndc),
                "retrieval/p50_ms": float(p50_b),
                "retrieval/p95_ms": float(p95_b),
                "count": len(idxs),
            }

    # Dump per-query results if requested
    if args.dump_results:
        os.makedirs(os.path.dirname(args.dump_results), exist_ok=True)
        with open(args.dump_results, "w", encoding="utf-8") as f:
            for row in per_query_dump:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # MLflow logging (optional)
    """if args.mlflow:
        mlflow.set_experiment(args.mlflow_experiment)
        with mlflow.start_run(run_name=f"eval-retrieval-{args.mode}"):
            tags = {
                "phase": "eval",
                "task": "retrieval",
                "mode": args.mode,
                "alpha": str(args.alpha) if args.mode == "hybrid" else "",
                "embed_model": args.embed_model,
                "db_collection": args.collection,
                "eval_set": args.tag_eval_set or os.path.basename(args.eval_file),
                "eval_sha256": sha256_file(args.eval_file),
                "k": str(args.k),
            }
            mlflow.set_tags(tags)
            for k, v in metrics.items():
                if isinstance(v, dict):
                    continue
                safe_k = k.replace("/", "_").replace("@", "at")
                try:
                    mlflow.log_metric(safe_k, float(v) if v is not None else float("nan"))
                except Exception:
                    # tolerate NaNs
                    pass
            # Save full metrics JSON
            out_json = json.dumps(metrics, indent=2)
            tmp_path = "./metrics_retrieval.json"
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(out_json)
            mlflow.log_artifact(tmp_path, artifact_path="eval")
            os.remove(tmp_path)
            if args.dump_results and os.path.exists(args.dump_results):
                mlflow.log_artifact(args.dump_results, artifact_path="eval")"""

    return metrics

# ================== CLI ==================
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--eval_file", type=str, required=True, help="JSONL eval file (must have query_text, gold_chunk_ids)")
    p.add_argument("--db_dir", type=str, required=True)
    p.add_argument("--collection", type=str, required=True)
    p.add_argument("--embed_model", type=str, default="jinaai/jina-embeddings-v3")
    p.add_argument("--device", type=str, default="cuda" if _CUDA else "cpu")
    p.add_argument("--k", type=int, default=50, help="top-k to fetch (min 10 for metrics)")
    p.add_argument("--by_strata", action="store_true", help="report metrics broken down by strata.type/issueArea/decade")
    p.add_argument("--text_key", type=str, default="text_clean", help="(kept for parity; not used by eval)")
    p.add_argument("--id_key", type=str, default="chunk_id", help="metadata key used as id in results")
    p.add_argument("--dump_results", type=str, default="", help="Path to write per-query results JSONL")
    p.add_argument("--max_queries", type=int, default=0, help="If >0, limit number of queries for a quick smoke run")

    # Retrieval mode knobs (match retriever.py)
    p.add_argument("--mode", choices=["dense", "bm25", "hybrid"], default="dense")
    p.add_argument("--alpha", type=float, default=0.6, help="hybrid weight for dense (0..1)")
    p.add_argument("--bm25_k", type=int, default=None, help="BM25 candidate pool (if HybridRetriever uses it)")
    p.add_argument("--dense_k", type=int, default=None, help="Dense candidate pool (if HybridRetriever uses it)")

    # MLflow
    #p.add_argument("--mlflow", action="store_true")
    #p.add_argument("--mlflow_experiment", type=str, default="legal-rag-main")
    #p.add_argument("--tag_eval_set", type=str, default="")

    args = p.parse_args()

    metrics = eval_retrieval(args)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()