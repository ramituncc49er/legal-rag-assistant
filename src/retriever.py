"""
retriever.py

Dense + Hybrid retrieval for legal_rag_assistant using:
- LangChain + LanceDB (dense ANN)
- Jina v3 HF embeddings (local)
- rank-bm25 (BM25)
- Optional CrossEncoder reranker (MiniLM by default)
- MLflow logging (latency + simple retrieval metrics, optional)

Usage examples
--------------
# 1) Build (ingest) index from a Parquet or JSONL of chunks
python retrieval_hybrid.py build \
  --data_path ./tables/opinion_chunks.parquet \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --text_key text_clean \
  --id_key chunk_id

# 2) Query dense-only
python retrieval_hybrid.py search \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --mode dense \
  --query "What did Scalia say about de novo review in Arvizu?" \
  --k 10

# 3) Query hybrid (dense+BM25) with alpha=0.65 and CrossEncoder rerank top 20 → return top 10
python retrieval_hybrid.py search \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --mode hybrid \
  --alpha 0.65 \
  --reranker cross-encoder/ms-marco-MiniLM-L-6-v2 \
  --rerank_top_n 20 \
  --k 10 \
  --query "Standard of review applied in United States v. Arvizu?"

# 4) Evaluate a list of queries (newline-delimited file); logs MLflow run
python retrieval_hybrid.py batch \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --mode hybrid \
  --alpha 0.6 \
  --queries_file ./eval/retrieval_eval_queries.txt \
  --k 20 \
  --mlflow_exp legal-rag-main \
  --mlflow_run_tag phase=1
"""

import os
import sys
import json
import time
import math
import argparse
import warnings
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd

#import mlflow

from langchain_community.vectorstores import LanceDB
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

import lancedb

from rank_bm25 import BM25Okapi

# ---- Reranker (optional) ----
from sentence_transformers import CrossEncoder


# ================== Utils ==================
def device_auto() -> str:
    """Pick CUDA if available, else CPU. Keeps things simple."""
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def read_chunks_any(data_path: str) -> pd.DataFrame:
    """
    Load chunk records (Parquet OR JSONL/JSON).
    Expects at minimum: text_clean, chunk_id
    Keeps additional metadata columns.
    """
    ext = os.path.splitext(data_path)[1].lower()
    
    with open(data_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, list):
        df = pd.DataFrame(payload)
    else:
        # single object with "data" key, etc.
        df = pd.DataFrame(payload.get("data", []))

    if "text_clean" not in df.columns or "chunk_id" not in df.columns:
        raise ValueError("Input must contain at least 'text_clean' and 'chunk_id' columns.")

    df["text_clean"] = df["text_clean"].astype(str).fillna("")
    return df


def build_documents(df: pd.DataFrame, text_key: str, id_key: str) -> List[Document]:
    """
    Convert rows to LangChain Documents with metadata. Keep a concise set of useful metadata fields.
    """
    keep_meta = ["chunk_id", "doc_id", "opinion_id", "case_id", "cl_cluster_id", "case_name", "type", "prev_chunk_id", "next_chunk_id", "votes", "created_at", "cl_url", "date_filed",  "us_cite", "sct_cite", "led_cite", "lexis_cite", "term", "decisionDirection", "decisionType", "majVotes", "minVotes", "majOpinWriter", "majOpinAssigner", "issue", "issueArea", "lawType", "lawSupp", "lawMinor"]
    docs = []
    for _, r in df.iterrows():
        md = {k: r[k] for k in keep_meta if k in df.columns}
        for k,v in list(md.items()):
            if isinstance(v, (np.floating, np.float32, np.float64)):
                md[k] = float(v)
            elif isinstance(v, (np.integer, np.int64, np.int32)):
                md[k] = int(v)
        md["chunk_id"] = md.get("chunk_id", r.get(id_key))
        docs.append(Document(page_content=str(r[text_key]), metadata=md))
    return docs

def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """Min-max normalize scores dict per query; safe for singletons."""
    if not scores:
        return scores
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    if math.isclose(hi, lo):
        return {k: 1.0 for k in scores}  # avoid div by zero; treat equal
    return {k: (v - lo) / (hi - lo) for k, v in scores.items()}

def invert_distance_to_sim(dist: float) -> float:
    """Convert vectorstore distance to similarity score (larger is better)."""
    # LanceDB returns L2 or cosine distance depending on index; treat smaller distance as higher sim.
    return 1.0 / (1.0 + float(dist))

# ================== Index / Retriever ==================
class HybridRetriever:
    """
    Dense (LanceDB) + optional BM25 hybrid retriever with α weighting and optional CrossEncoder rerank.
    """
    def __init__(
        self,
        db_dir: str,
        collection_name: str,
        embed_model_name: str = "jinaai/jina-embeddings-v3",
        bm25_enabled: bool = True,
        reranker_model: Optional[str] = None,
        hf_device: Optional[str] = None
    ):
        self.db_dir = db_dir
        self.collection_name = collection_name
        self.device = hf_device or device_auto()

        # Embeddings
        '''self.embeddings = HuggingFaceEmbeddings(
            model_name=embed_model_name,
            model_kwargs={"device": self.device}
        )'''

        self.embeddings = HuggingFaceEmbeddings(
            model_name=embed_model_name,
            model_kwargs={
                "device": self.device,
                "trust_remote_code": True  # required for Jina v3 family
            }
        )

        # LanceDB connection & vector store
        self.conn = lancedb.connect(self.db_dir)
        # Will raise if collection not found; caller ensures build before search (or create)
        tbl = self.conn.open_table(self.collection_name)
        self.vs = LanceDB(connection=self.conn, table_name=self.collection_name, embedding=self.embeddings)

        # Load all docs into memory for BM25 (optional) and metadata lookup
        self._id_to_doc: Dict[str, Document] = {}
        self._bm25 = None
        if bm25_enabled:
            self._prepare_bm25()

        # Optional CrossEncoder reranker
        self.reranker = None
        if reranker_model:
            self.reranker = CrossEncoder(reranker_model, device=self.device)

    def _prepare_bm25(self):
        # Pull raw rows from the LanceDB table for BM25 corpus and metadata map
        table = self.conn.open_table(self.collection_name)
        rows = list(table.to_pandas().itertuples(index=False))
        corpus = []
        id_list = []
        for row in rows:
            # row has columns: 'vector', 'text', 'metadata' in LanceDB schema (LangChain default)
            text = getattr(row, "text", "") or ""
            md = getattr(row, "metadata", {}) or {}
            cid = md.get("chunk_id")
            if not cid:
                continue
            id_list.append(cid)
            corpus.append(text)
            # Build id→Document map once
            if cid not in self._id_to_doc:
                self._id_to_doc[cid] = Document(page_content=text, metadata=md)

        # Tokenize simply (split by whitespace); BM25Okapi expects list of tokens
        tokenized = [t.split() for t in corpus]
        self._bm25 = BM25Okapi(tokenized)
        self._bm25_id_list = id_list

    # Retrieval
    def search_dense(self, query: str, k: int = 20) -> List[Tuple[str, float]]:
        """
        Return list of (chunk_id, score) using LanceDB similarity search_with_score.
        Larger score is better (we invert distance).
        """
        docs_scores = self.vs.similarity_search_with_score(query, k=k)
        out: List[Tuple[str, float]] = []
        for doc, dist in docs_scores:
            cid = doc.metadata.get("chunk_id")
            if cid:
                out.append((cid, invert_distance_to_sim(dist)))
                self._id_to_doc[cid] = self._id_to_doc.get(cid, doc)
        return out

    def search_bm25(self, query: str, k: int = 20) -> List[Tuple[str, float]]:
        if not self._bm25:
            return []
        scores = self._bm25.get_scores(query.split())
        # pick top-k indices
        idxs = np.argsort(scores)[::-1][:k]
        out = []
        for i in idxs:
            cid = self._bm25_id_list[i]
            out.append((cid, float(scores[i])))
        return out

    def search_hybrid(
        self,
        query: str,
        k: int = 20,
        alpha: float = 0.6,
        bm25_k: Optional[int] = None,
        dense_k: Optional[int] = None
    ) -> List[Tuple[str, float]]:
        """
        Combine dense and BM25 via normalized linear blend:
        score = alpha * dense + (1-alpha) * bm25
        """
        dense_k = dense_k or k
        bm25_k = bm25_k or k

        dense_pairs = self.search_dense(query, k=dense_k)
        bm25_pairs  = self.search_bm25(query, k=bm25_k)

        d_map = {cid: s for cid, s in dense_pairs}
        b_map = {cid: s for cid, s in bm25_pairs}

        d_norm = normalize_scores(d_map)
        b_norm = normalize_scores(b_map)

        # Union and combine
        all_ids = set(d_norm) | set(b_norm)
        combo = {}
        for cid in all_ids:
            ds = d_norm.get(cid, 0.0)
            bs = b_norm.get(cid, 0.0)
            combo[cid] = alpha * ds + (1.0 - alpha) * bs

        ranked = sorted(combo.items(), key=lambda x: x[1], reverse=True)[:k]
        return ranked

    def rerank(self, query: str, candidates: List[Tuple[str, float]], top_n: int) -> List[Tuple[str, float]]:
        """
        Apply CrossEncoder reranking on the top-N candidates and return re-ordered list.
        """
        if not self.reranker or not candidates:
            return candidates

        top_n = min(top_n, len(candidates))
        ids = [cid for cid, _ in candidates[:top_n]]
        texts = [self._id_to_doc[cid].page_content for cid in ids]
        # CrossEncoder expects list of (query, text)
        pairs = list(zip([query]*len(texts), texts))
        scores = self.reranker.predict(pairs)  # higher is better

        rescored = list(zip(ids, [float(s) for s in scores]))
        rescored.sort(key=lambda x: x[1], reverse=True)
        # keep original scores for the tail (if any)
        rescored_ids = set(i for i,_ in rescored)
        tail = [(cid, s) for cid, s in candidates if cid not in rescored_ids]
        out = rescored + tail
        return out

    def fetch_docs(self, id_score_pairs: List[Tuple[str, float]]) -> List[Document]:
        docs = []
        for cid, score in id_score_pairs:
            d = self._id_to_doc.get(cid)
            if d is not None:
                # stash score in metadata for downstream display
                md = dict(d.metadata)
                md["_score"] = float(score)
                docs.append(Document(page_content=d.page_content, metadata=md))
        return docs

# ================== Build helpers ==================
def build_lancedb_index(
    data_path: str,
    db_dir: str,
    collection_name: str,
    text_key: str = "text_clean",
    id_key: str = "chunk_id",
    embed_model_name: str = "jinaai/jina-embeddings-v3",
    hf_device: Optional[str] = None,
    recreate: bool = False,
) -> Tuple[LanceDB, int]:
    """
    Create or update LanceDB index with embeddings.
    """
    device = hf_device or device_auto()

    embeddings = HuggingFaceEmbeddings(
            model_name=embed_model_name,
            model_kwargs={
                "device": device,
                "trust_remote_code": True  # required for Jina v3 family
            },
            encode_kwargs={"normalize_embeddings": True}
        )

    df = read_chunks_any(data_path)
    docs = build_documents(df, text_key=text_key, id_key=id_key)

    os.makedirs(db_dir, exist_ok=True)
    conn = lancedb.connect(db_dir)

    if recreate and collection_name in conn.table_names():
        conn.drop_table(collection_name)

    # Create or open via LangChain VectorStore wrapper
    vs = LanceDB.from_documents(
        documents=docs,
        embedding=embeddings,
        connection=conn,
        table_name=collection_name
    )
    return vs, len(docs)

def cmd_build(args):
    t0 = time.time()
    vs, n = build_lancedb_index(
        data_path=args.data_path,
        db_dir=args.db_dir,
        collection_name=args.collection,
        text_key=args.text_key,
        id_key=args.id_key,
        embed_model_name=args.embed_model,
        hf_device=args.device,
        recreate=args.recreate,
    )
    dt = time.time() - t0
    print(f"[build] Indexed {n} docs into '{args.collection}' at '{args.db_dir}' in {dt:.2f}s.")

def pretty_doc(doc: Document, rank: int):
    md = doc.metadata
    title = md.get("case_name") or md.get("us_cite") or "Unknown"
    cid = md.get("chunk_id")
    cite = md.get("us_cite")
    url = md.get("cl_url")
    typ = md.get("type")
    score = md.get("_score")
    snippet = doc.page_content[:300].replace("\n", " ")
    print(f"{rank:>2}. [{score:.4f}] chunk_id={cid} | {title} | type={typ} | cite={cite} | url={url}")
    print(f"    {snippet} ...\n")

def run_single_query(args):
    retr = HybridRetriever(
        db_dir=args.db_dir,
        collection_name=args.collection,
        embed_model_name=args.embed_model,
        bm25_enabled=(args.mode in ["bm25", "hybrid"]),
        reranker_model=args.reranker,
        hf_device=args.device,
    )

    t0 = time.time()
    if args.mode == "dense":
        id_scores = retr.search_dense(args.query, k=args.k)
    elif args.mode == "bm25":
        id_scores = retr.search_bm25(args.query, k=args.k)
    elif args.mode == "hybrid":
        id_scores = retr.search_hybrid(
            query=args.query, k=args.k,
            alpha=args.alpha,
            bm25_k=args.bm25_k,
            dense_k=args.dense_k
        )
    else:
        raise ValueError(f"Unknown mode: {args.mode}")

    # Optional rerank
    if args.reranker and id_scores:
        id_scores = retr.rerank(args.query, id_scores, top_n=args.rerank_top_n)[:args.k]

    dt = (time.time() - t0) * 1000.0
    docs = retr.fetch_docs(id_scores[:args.k])

    print(f"\n== Results (mode={args.mode}, k={args.k}, reranker={bool(args.reranker)}) | latency={dt:.1f} ms ==")
    for i, d in enumerate(docs, start=1):
        pretty_doc(d, i)

def run_batch_queries(args):
    # Read queries
    with open(args.queries_file, "r", encoding="utf-8") as f:
        queries = [ln.strip() for ln in f if ln.strip()]

    retr = HybridRetriever(
        db_dir=args.db_dir,
        collection_name=args.collection,
        embed_model_name=args.embed_model,
        bm25_enabled=(args.mode in ["bm25", "hybrid"]),
        reranker_model=args.reranker,
        hf_device=args.device,
    )

    latencies_ms = []
    k = args.k

    # Optional MLflow
    """run = None
    if args.mlflow_exp:
        mlflow.set_tracking_uri("file:./mlruns")
        mlflow.set_experiment(args.mlflow_exp)
        run = mlflow.start_run()
        # params
        mlflow.log_params({
            "mode": args.mode,
            "alpha": args.alpha,
            "k": args.k,
            "bm25_k": args.bm25_k,
            "dense_k": args.dense_k,
            "reranker": args.reranker or "none",
            "rerank_top_n": args.rerank_top_n,
            "embed_model": args.embed_model,
            "device": args.device or device_auto(),
            "db_dir": args.db_dir,
            "collection": args.collection
        })
        # tags
        if args.mlflow_run_tag:
            key, _, val = args.mlflow_run_tag.partition("=")
            if key and val:
                mlflow.set_tag(key, val)"""

    for q in queries:
        t0 = time.time()
        if args.mode == "dense":
            id_scores = retr.search_dense(q, k=k)
        elif args.mode == "bm25":
            id_scores = retr.search_bm25(q, k=k)
        else:
            id_scores = retr.search_hybrid(
                query=q, k=k, alpha=args.alpha,
                bm25_k=args.bm25_k, dense_k=args.dense_k
            )

        if args.reranker and id_scores:
            id_scores = retr.rerank(q, id_scores, top_n=args.rerank_top_n)[:k]

        dt = (time.time() - t0) * 1000.0
        latencies_ms.append(dt)

    # Log simple latency stats
    p50 = float(np.percentile(latencies_ms, 50)) if latencies_ms else 0.0
    p95 = float(np.percentile(latencies_ms, 95)) if latencies_ms else 0.0
    print(f"[batch] n={len(queries)} | p50={p50:.1f} ms | p95={p95:.1f} ms")
    #if run:
    #    mlflow.log_metrics({"retrieve_p50_ms": p50, "retrieve_p95_ms": p95})
    #    mlflow.end_run()

# ================== CLI ==================
def main():
    parser = argparse.ArgumentParser(description="Dense + Hybrid Retrieval (LangChain + LanceDB + Jina v3 + BM25 + optional reranker)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # build
    p_build = sub.add_parser("build", help="Build (ingest) LanceDB index from chunks")
    p_build.add_argument("--data_path", required=True, help="JSON, or JSONL with chunk records")
    p_build.add_argument("--db_dir", required=True, help="Directory for LanceDB database")
    p_build.add_argument("--collection", required=True, help="Collection (table) name")
    p_build.add_argument("--text_key", default="text_clean")
    p_build.add_argument("--id_key", default="chunk_id")
    p_build.add_argument("--embed_model", default="jinaai/jina-embeddings-v3")
    p_build.add_argument("--device", default=None, help="Force device: cuda|cpu (auto if omitted)")
    p_build.add_argument("--recreate", action="store_true", help="Drop & recreate collection")
    p_build.set_defaults(func=cmd_build)

    # search (single query)
    p_search = sub.add_parser("search", help="Run a single query")
    p_search.add_argument("--db_dir", required=True)
    p_search.add_argument("--collection", required=True)
    p_search.add_argument("--mode", choices=["dense", "bm25", "hybrid"], default="hybrid")
    p_search.add_argument("--alpha", type=float, default=0.6, help="Hybrid weight for dense (0..1)")
    p_search.add_argument("--bm25_k", type=int, default=None, help="BM25 candidate count (defaults to k)")
    p_search.add_argument("--dense_k", type=int, default=None, help="Dense candidate count (defaults to k)")
    p_search.add_argument("--k", type=int, default=20, help="final results to return")
    p_search.add_argument("--embed_model", default="jinaai/jina-embeddings-v3")
    p_search.add_argument("--reranker", default=None, help="CrossEncoder model name (e.g., cross-encoder/ms-marco-MiniLM-L-6-v2)")
    p_search.add_argument("--rerank_top_n", type=int, default=20, help="Top-N candidates to rerank before returning k")
    p_search.add_argument("--device", default=None)
    p_search.add_argument("--query", required=True)
    p_search.set_defaults(func=lambda a: run_single_query(a))

    # batch (multiple queries + MLflow)
    p_batch = sub.add_parser("batch", help="Run a batch of queries; logs latencies to MLflow")
    p_batch.add_argument("--db_dir", required=True)
    p_batch.add_argument("--collection", required=True)
    p_batch.add_argument("--mode", choices=["dense", "bm25", "hybrid"], default="hybrid")
    p_batch.add_argument("--alpha", type=float, default=0.6)
    p_batch.add_argument("--bm25_k", type=int, default=None)
    p_batch.add_argument("--dense_k", type=int, default=None)
    p_batch.add_argument("--k", type=int, default=20)
    p_batch.add_argument("--embed_model", default="jinaai/jina-embeddings-v3")
    p_batch.add_argument("--reranker", default=None)
    p_batch.add_argument("--rerank_top_n", type=int, default=20)
    p_batch.add_argument("--device", default=None)
    p_batch.add_argument("--queries_file", required=True, help="One query per line")
    #p_batch.add_argument("--mlflow_exp", default=None, help="MLflow experiment name")
    #p_batch.add_argument("--mlflow_run_tag", default=None, help="Optional single tag: key=value")
    p_batch.set_defaults(func=lambda a: run_batch_queries(a))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
