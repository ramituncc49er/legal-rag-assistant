"""
inference.py

- Inputs: queries JSONL (query_id, query_text, reference_answer, ...)
- Retrieval: HybridRetriever (dense+bm25) via retriever.py
- Context building:
    * Chunk text (truncated)
    * ALL metadata fields (compact k=v; truncation configurable)
    * SCDB codebook snippets fetched from a markdown file via in-memory keyword index
- Prompting:
    * Uses chat template (system + user) for instruct models (Mistral/Llama)
    * System message = stable rules; User message = SCDB notes + Context + Question
- Outputs: JSONL with reference_answer, generated_answer, pred_chunk_ids, latencies
"""

import argparse
import json
import os
import re
import time
import hashlib
from functools import lru_cache
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import sys
sys.path.append(os.path.dirname(__file__))
from retriever import HybridRetriever

#import mlflow

try:
    import torch
    _CUDA = torch.cuda.is_available()
except Exception:
    _CUDA = False

# --- HF Transformers (local inference) ---
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers.generation.utils import GenerationConfig

# ================== Helpers ==================
def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ================== Codebook (markdown) helpers ==================
@lru_cache(maxsize=1)
def load_codebook_md(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _split_md_sections(md_text: str) -> List[Dict[str, str]]:
    parts = re.split(r"(?m)^##?\s+", md_text)
    sections = []
    if parts and not parts[0].strip().startswith(("##", "#")):
        lead = parts[0].strip()
        if lead:
            sections.append({"title": "Intro", "body": lead})
        parts = parts[1:]
    for p in parts:
        lines = p.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        sections.append({"title": title, "body": body})
    return sections

def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def build_codebook_index(md_text: str):
    sections = _split_md_sections(md_text)
    inv = defaultdict(set)
    for i, sec in enumerate(sections):
        blob = f"{sec['title']} {sec['body']}"
        toks = set(_normalize(blob).split())
        for t in toks:
            if len(t) >= 2:
                inv[t].add(i)
    return sections, inv

def _score_section(query_terms: List[str], section: Dict[str, str]) -> int:
    title = _normalize(section["title"])
    body = _normalize(section["body"])
    tset = title.split()
    bset = body.split()
    score = 0
    for q in query_terms:
        if not q:
            continue
        score += 3 * tset.count(q)
        score += 1 * bset.count(q)
    return score

def retrieve_codebook_snippets(md_text: str, terms: List[str],
                               top_n: int = 2, max_chars_per_snippet: int = 600) -> List[str]:
    sections, inv = build_codebook_index(md_text)
    q_terms = [_normalize(t) for t in terms if t]
    cand_ids = set()
    for qt in q_terms:
        if qt in inv:
            cand_ids |= inv[qt]
    if not cand_ids:
        alts = set()
        for t in q_terms:
            alts.add(t.replace("_", " "))
            alts.add(re.sub(r"cite$", "citation", t))
        for a in alts:
            if a in inv:
                cand_ids |= inv[a]
    if not cand_ids:
        cand_ids = set(range(len(sections)))

    scored = []
    for i in cand_ids:
        sc = _score_section(q_terms, sections[i])
        if sc > 0:
            scored.append((sc, i))
    scored.sort(reverse=True)

    out = []
    for _, i in scored[:top_n]:
        title = sections[i]["title"]
        body = sections[i]["body"]
        snippet = f"### SCDB: {title}\n{body}"
        if len(snippet) > max_chars_per_snippet:
            snippet = snippet[:max_chars_per_snippet] + "…"
        out.append(snippet)
    return out

# ================== Context / prompt builders ==================
def format_doc_for_context(
    doc,
    include_meta: bool = True,
    max_chars: int = 1200,
    meta_max_value_chars: int = 200,
    meta_sort_keys: bool = True
) -> str:
    """Format a retrieved Document into a context string (with all metadata)."""
    text = (doc.page_content or "")[:max_chars]
    if not include_meta:
        return text

    md = doc.metadata or {}
    items = sorted(md.items(), key=lambda kv: kv[0]) if meta_sort_keys else md.items()

    meta_bits = []
    for k, v in items:
        try:
            v_str = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
        except Exception:
            v_str = repr(v)
        if meta_max_value_chars and len(v_str) > meta_max_value_chars:
            v_str = v_str[:meta_max_value_chars] + "…"
        meta_bits.append(f"{k}={v_str}")

    meta_str = (" [" + "; ".join(meta_bits) + "]") if meta_bits else ""
    return f"{text}{meta_str}"

def enrich_with_codebook(doc, codebook_md_or_path: str,
    keys_of_interest: Tuple[str, ...] = (
        "case_id", "case_name", "type", "votes", "cl_url", "date_filed", "us_cite", "sct_cite", "led_cite", "lexis_cite", "term",
        "decisionDirection","decisionType","majVotes","minVotes", "majOpinWriter","majOpinAssigner","issue","issueArea",
        "lawType","lawSupp","lawMinor"
    ), top_n: int = 2, max_total_chars: int = 900) -> str:
    if not codebook_md_or_path:
        return ""
    if os.path.exists(codebook_md_or_path):
        md_text = load_codebook_md(codebook_md_or_path)
    else:
        md_text = codebook_md_or_path

    md = doc.metadata or {}
    terms = []
    for k in keys_of_interest:
        if k in md and md[k] not in (None, "", []):
            terms.append(k)
            if k.endswith("_cite"): terms.append("citation")
            if k == "us_cite": terms += ["U.S. Reporter Citation", "US Reports"]
            if k == "sct_cite": terms.append("Supreme Court Reporter")
            if k == "led_cite": terms.append("Lawyers' Edition")
            if k == "lexis_cite": terms.append("LEXIS cite")
            if k in ("issue","issueArea"): terms.append("issue area")
            if k == "decisionType": terms.append("decision type")
            if k == "term": terms.append("term (Court Term)")

    if not terms:
        return ""

    per_snip = max_total_chars // max(1, top_n)
    snippets = retrieve_codebook_snippets(md_text, terms, top_n=top_n, max_chars_per_snippet=per_snip)
    if not snippets:
        return ""
    block = "\n".join(snippets)
    if len(block) > max_total_chars:
        block = block[:max_total_chars] + "…"
    return block

def collect_global_scdb_snippets(docs, codebook_md_or_path: str,
                                 per_doc_chars: int = 400,
                                 max_total_chars: int = 1200) -> str:
    """Aggregate small SCDB snippets across top docs and deduplicate."""
    if not codebook_md_or_path:
        return ""
    seen = set()
    pieces = []
    for d in docs:
        snip = enrich_with_codebook(d, codebook_md_or_path, top_n=1, max_total_chars=per_doc_chars)
        if not snip:
            continue
        for part in snip.split("\n\n"):
            key = _normalize(part)
            if key and key not in seen:
                seen.add(key)
                pieces.append(part.strip())
        if sum(len(p) for p in pieces) >= max_total_chars:
            break
    joined = "\n\n".join(pieces)
    if len(joined) > max_total_chars:
        joined = joined[:max_total_chars] + "…"
    return joined

"""def build_messages_from_file(system_prompt_text: str,
                             query_text: str,
                             context_blocks: str,
                             scdb_snippets: str):
    user_payload = (
        "Question:\n"
        f"{query_text.strip()}\n\n"
        "Context:\n"
        f"{context_blocks.strip()}\n\n"
        "SCDB Codebook Notes (for interpreting metadata only; do not treat as factual case text):\n"
        f"{(scdb_snippets or '').strip()}\n\n"
        "Answer:"
    )
    messages = [
        {"role": "system", "content": system_prompt_text.strip()},
        {"role": "user",   "content": user_payload}
    ]
    return messages"""

# ********** Updated for Ollama models **********

def build_messages_from_file(system_prompt_text: str,
                             query_text: str,
                             context_blocks: str,
                             scdb_snippets: str):
    user_payload = (
        "Question:\n"
        f"{query_text.strip()}\n\n"
        "You are given the following legal context (U.S. Supreme Court chunks):\n"
        f"{context_blocks.strip()}\n\n"
        "Based only on this context, write your answer to the given question in the format specified by the system message.\n"
    )
    messages = [
        {"role": "system", "content": system_prompt_text.strip()},
        {"role": "user",   "content": user_payload}
    ]
    return messages


# ================== Model loading / generation ==================
def load_model_and_tokenizer(
    model_name: str,
    device: str = "cuda",
    use_fast_tokenizer: bool = True,
    load_in_4bit: bool = True,
    load_in_8bit: bool = False,
    dtype: str = "float16"
):
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True, trust_remote_code=True)
    if tok.pad_token is None and tok.eos_token is not None:
        tok.pad_token = tok.eos_token

    torch_dtype = torch.float16 if dtype == "float16" else torch.bfloat16

    # Quantization config (bitsandbytes)
    quant_cfg = None
    if load_in_4bit:
        quant_cfg = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch_dtype,
        )
    elif load_in_8bit:
        quant_cfg = BitsAndBytesConfig(load_in_8bit=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch_dtype,
        quantization_config=quant_cfg,   # None = full precision
        device_map="auto",               # shard/dispatch automatically
        low_cpu_mem_usage=True,
    )
    model.eval()
    return model, tok

def generate_answer_chat(model, tok, messages,
                         device="cuda",
                         max_new_tokens=256,
                         temperature=0.0,
                         top_p=1.0) -> str:
    prompt = tok.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_device = next(model.parameters()).device
    inputs = tok(prompt, return_tensors="pt", truncation=True).to(model_device)

    gen_cfg = GenerationConfig(
        max_new_tokens=max_new_tokens,
        do_sample=(temperature > 0.0),
        temperature=temperature,
        top_p=top_p,
        eos_token_id=tok.eos_token_id,
        pad_token_id=tok.pad_token_id,
    )

    model.eval()
    with torch.no_grad():
        out = model.generate(**inputs, generation_config=gen_cfg)

    input_len = inputs["input_ids"].shape[-1]
    gen_tokens = out[0][input_len:]
    text = tok.decode(gen_tokens, skip_special_tokens=True)
    return text.strip()

# **************** OpenAI-compatible chat generator (Ollama, LM Studio, vLLM, etc.) ****************
def generate_answer_chat_openai(
    messages,
    model_name: str,
    base_url: str,
    api_key: str,
    max_new_tokens: int = 256,
    temperature: float = 0.4,
    top_p: float = 1.0,
):
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key)
    resp = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_new_tokens,   # OpenAI-style name
    )
    return resp.choices[0].message.content.strip()

# ================== Run inference ==================
def run_inference_on_queries(args):
    rows = load_jsonl(args.queries_file)
    if args.max_queries and args.max_queries > 0:
        rows = rows[:args.max_queries]

    retr = HybridRetriever(
        db_dir=args.db_dir,
        collection_name=args.collection,
        embed_model_name=args.embed_model,
        bm25_enabled=True,
        reranker_model=None,
        hf_device=args.device
    )

    # Load SCDB codebook
    codebook_md = ""
    if args.codebook_md_path:
        codebook_md = load_codebook_md(args.codebook_md_path) if os.path.exists(args.codebook_md_path) else args.codebook_md_path

    # Load SYSTEM prompt (stable rules)
    with open(args.prompt_file, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    model, tok = load_model_and_tokenizer(args.model_name, device=args.device)
    results = []

    for i, row in enumerate(rows):
        qid = row.get("query_id", f"q{i:04d}")
        qtext = row["query_text"]
        ref_answer = row.get("reference_answer", "")

        # Retrieval
        t0 = time.time()
        id_scores = retr.search_hybrid(
            query=qtext, k=args.k, alpha=args.alpha,
            bm25_k=args.bm25_k, dense_k=args.dense_k
        )
        docs = retr.fetch_docs(id_scores)
        ret_ms = (time.time() - t0) * 1000.0

        # Build context blocks
        context_blocks = []
        for idx, d in enumerate(docs[:args.max_context_docs], start=1):
            block = format_doc_for_context(
                d, include_meta=not args.strip_meta,
                meta_max_value_chars=args.meta_max_value_chars
            )
            # (Optional) keep per-doc SCDB enrichment directly inside each block
            if args.per_doc_scdb:
                cb = enrich_with_codebook(d, codebook_md, top_n=2, max_total_chars=900)
                if cb:
                    block += "\n" + cb
            context_blocks.append(f"[{idx}] {block}")
        context_text = "\n\n".join(context_blocks)

        # Global SCDB snippets (recommended if per-doc is off; harmless if both)
        global_scdb = ""
        if codebook_md and args.global_scdb:
            global_scdb = collect_global_scdb_snippets(docs[:args.max_context_docs], codebook_md)

        # Build chat messages (system + user)
        messages = build_messages_from_file(system_prompt, qtext, context_text, global_scdb)

        # Generate answer
        t1 = time.time()
        gen_answer = generate_answer_chat(
            model, tok, messages, device=args.device,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_p=args.top_p
        )
        gen_ms = (time.time() - t1) * 1000.0

        results.append({
            "query_id": qid,
            "query_text": qtext,
            "reference_answer": ref_answer,
            "generated_answer": gen_answer,
            "pred_chunk_ids": [cid for cid, _ in id_scores],
            "retrieval_latency_ms": ret_ms,
            "generation_latency_ms": gen_ms,
            "retrieval": {
                "mode": "hybrid",
                "alpha": args.alpha,
                "k": args.k,
                "dense_k": args.dense_k,
                "bm25_k": args.bm25_k,
                "embed_model": args.embed_model,
                "collection": args.collection
            },
            "model_name": args.model_name,
        })

        if args.print_prompt:
            print("SYSTEM:\n" + system_prompt.strip())
            print("-"*80)
            print("USER:\n" + messages[1]["content"])
            print("="*80)
            print("MODEL RESPONSE:\n" + gen_answer)
            print("="*80 + "\n")

        if args.verbose:
            print(f"[{i+1}/{len(rows)}] {qid} | ret={ret_ms:.1f} ms | gen={gen_ms:.1f} ms")

    # Save results
    if args.out_jsonl:
        os.makedirs(os.path.dirname(args.out_jsonl) or ".", exist_ok=True)
        with open(args.out_jsonl, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    return results

# ================== CLI ==================
def main():
    p = argparse.ArgumentParser(description="Legal RAG Inference (Instruct Chat)")
    p.add_argument("--queries_file", required=True)
    p.add_argument("--db_dir", required=True)
    p.add_argument("--collection", required=True)
    p.add_argument("--embed_model", default="jinaai/jina-embeddings-v3")
    p.add_argument("--device", default="cuda" if _CUDA else "cpu")

    p.add_argument("--k", type=int, default=50)
    p.add_argument("--alpha", type=float, default=0.6)
    p.add_argument("--dense_k", type=int, default=120)
    p.add_argument("--bm25_k", type=int, default=200)

    p.add_argument("--codebook_md_path", default="")
    p.add_argument("--prompt_file", required=True,
                   help="Path to SYSTEM rules text (no placeholders).")
    p.add_argument("--max_context_docs", type=int, default=8)
    p.add_argument("--strip_meta", action="store_true")
    p.add_argument("--meta_max_value_chars", type=int, default=200)
    p.add_argument("--per_doc_scdb", action="store_true",
                   help="Append small SCDB snippets inside each context block.")
    p.add_argument("--global_scdb", action="store_true",
                   help="Add a consolidated SCDB section at top of the user message.")

    p.add_argument("--model_name", default="mistralai/Mistral-7B-Instruct-v0.3")
    p.add_argument("--max_new_tokens", type=int, default=256)
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--top_p", type=float, default=1.0)

    p.add_argument("--out_jsonl", default="./outputs/inference_results.jsonl")
    p.add_argument("--max_queries", type=int, default=0)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--print_prompt", action="store_true")

    args = p.parse_args()
    _ = run_inference_on_queries(args)

if __name__ == "__main__":
    main()