"""
rag_engine.py
"""
import os, sys
import time
from typing import Any, Dict, List, Tuple

from retriever import HybridRetriever

from inference import (
    build_messages_from_file,
    format_doc_for_context,
    collect_global_scdb_snippets,
    load_model_and_tokenizer,
    generate_answer_chat,
    load_codebook_md,
)

from config import set_default_env
set_default_env()

def _get_bool(env_key: str, default: bool = False) -> bool:
    return os.getenv(env_key, str(default).lower()).strip().lower() in ("1", "true", "yes", "y", "on")


class RAGEngine:
    def __init__(self):
        # ================== Retrieval config ==================
        self.db_dir: str = os.getenv("DB_DIR", "default")
        self.collection: str = os.getenv("COLLECTION", "default")
        self.embed_model: str = os.getenv("EMBED_MODEL", "jinaai/jina-embeddings-v3")
        self.device: str = os.getenv("DEVICE", "cpu")

        self.k: int = int(os.getenv("K", "50"))
        self.alpha: float = float(os.getenv("ALPHA", "0.6"))
        self.dense_k: int = int(os.getenv("DENSE_K", "120"))
        self.bm25_k: int = int(os.getenv("BM25_K", "200"))

        # ================== Context config ==================
        self.max_context_docs: int = int(os.getenv("MAX_CONTEXT_DOCS", "8"))
        self.strip_meta: bool = _get_bool("STRIP_META", False)
        self.meta_max_value_chars: int = int(os.getenv("META_MAX_VALUE_CHARS", "200"))
        self.global_scdb: bool = _get_bool("GLOBAL_SCDB", False)
        self.per_doc_scdb: bool = _get_bool("PER_DOC_SCDB", False)
        self.codebook_md_path: str = os.getenv("CODEBOOK_MD_PATH", "")

        # ================== Prompt / model config ==================
        self.prompt_file: str = os.getenv("PROMPT_FILE", "/Users/innerpiece92/Desktop/Project_Workspace/legal_rag_assistant/prompt/prompt_for_legal_assistant_base.txt")
        self.model_name: str = os.getenv("MODEL_NAME", "mistral:7b-instruct")
        self.max_new_tokens: int = int(os.getenv("MAX_NEW_TOKENS", "256"))
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.4"))
        self.top_p: float = float(os.getenv("TOP_P", "1.0"))
        self.load_in_4bit: bool = _get_bool("LOAD_IN_4BIT", True)
        self.load_in_8bit: bool = _get_bool("LOAD_IN_8BIT", False)
        self.dtype: str = os.getenv("DTYPE", "float16")
            
        # ================== Debug / logging config ==================
        self.print_context: bool = _get_bool("PRINT_CONTEXT", False)
        self.print_prompt: bool = _get_bool("PRINT_PROMPT", False)
            
        # ================== Ollama config ==================
        self.backend: str = os.getenv("LLM_BACKEND", "transformers").lower()  # "transformers" | "openai_compatible"
        self.openai_base_url: str = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "ollama")

        # ================== Instantiate components ==================
        self.retriever = HybridRetriever(
            db_dir=self.db_dir,
            collection_name=self.collection,
            embed_model_name=self.embed_model,
            bm25_enabled=True,
            reranker_model=None,
            hf_device=self.device,
        )

        # Load system prompt
        if not os.path.exists(self.prompt_file):
            raise FileNotFoundError(f"PROMPT_FILE not found: {self.prompt_file}")
        with open(self.prompt_file, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        # Optional SCDB codebook (load lazily at first use via load_codebook_md)
        self._codebook_loaded_text = None
        if self.codebook_md_path and os.path.exists(self.codebook_md_path):
            # warm the cache once to avoid disk I/O on first request
            self._codebook_loaded_text = load_codebook_md(self.codebook_md_path)

        """# Load model/tokenizer once
        self.model, self.tok = load_model_and_tokenizer(
            self.model_name,
            device=self.device,
            load_in_4bit=self.load_in_4bit,
            load_in_8bit=self.load_in_8bit,
            dtype=self.dtype,
        )"""
        
        # Load model/tokenizer once (ONLY for transformers backend)
        self.model, self.tok = (None, None)
        if self.backend == "transformers":
            self.model, self.tok = load_model_and_tokenizer(
                self.model_name,
                device=self.device,
                load_in_4bit=self.load_in_4bit,
                load_in_8bit=self.load_in_8bit,
                dtype=self.dtype,
            )

    # ================== Helpers ==================
    def _format_context(self, docs) -> Tuple[str, str]:
        """
        Returns (context_text, global_scdb_text)
        """
        context_blocks: List[str] = []
        for idx, d in enumerate(docs[: self.max_context_docs], start=1):
            block = format_doc_for_context(
                d,
                include_meta=not self.strip_meta,
                meta_max_value_chars=self.meta_max_value_chars,
            )
            if self.per_doc_scdb and self.codebook_md_path:
                # Keep per-doc SCDB enrichment consistent with inference.py
                from inference import enrich_with_codebook  # local import to avoid clutter

                cb = enrich_with_codebook(d, self._codebook_loaded_text or self.codebook_md_path,
                                          top_n=2, max_total_chars=900)
                if cb:
                    block += "\n" + cb
            context_blocks.append(f"[{idx}] {block}")

        context_text = "\n\n".join(context_blocks)

        global_scdb = ""
        if self.global_scdb and self.codebook_md_path:
            global_scdb = collect_global_scdb_snippets(
                docs[: self.max_context_docs],
                self._codebook_loaded_text or self.codebook_md_path,
            )
        return context_text, global_scdb

    @staticmethod
    def _safe_get(md: Dict[str, Any], key: str, default=None):
        try:
            return md.get(key, default)
        except Exception:
            return default

    def answer(self, q: str) -> Dict[str, Any]:
        """
        Run retrieval -> build context -> build chat messages -> generate answer.
        Returns: dict with `answer`, `latency_sec`, `sources`, and timing breakdowns.
        """
        t_all = time.time()

        # ================== Retrieval ==================
        t0 = time.time()
        id_scores = self.retriever.search_hybrid(
            query=q,
            k=self.k,
            alpha=self.alpha,
            bm25_k=self.bm25_k,
            dense_k=self.dense_k,
        )
        docs = self.retriever.fetch_docs(id_scores)
        ret_ms = (time.time() - t0) * 1000.0

        context_text, global_scdb = self._format_context(docs)
        messages = build_messages_from_file(self.system_prompt, q, context_text, global_scdb)
        
        if self.print_prompt:
            # Match inference.py style
            print("SYSTEM:\n" + self.system_prompt.strip())
            print("-" * 80)
            # messages[1] is always the user message in build_messages_from_file
            user_msg = messages[1]["content"] if len(messages) > 1 else ""
            print("USER:\n" + user_msg)
            print("=" * 80)

        # ================== Generation ==================
        t1 = time.time()
        """gen_answer = generate_answer_chat(
            self.model,
            self.tok,
            messages,
            device=self.device,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
        )"""
        if self.backend == "transformers":
            gen_answer = generate_answer_chat(
                self.model,
                self.tok,
                messages,
                device=self.device,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
            )
        else:
            # openai_compatible (Ollama)
            from inference import generate_answer_chat_openai
            
            gen_answer = generate_answer_chat_openai(
                messages=messages,
                model_name=self.model_name,
                base_url=self.openai_base_url,
                api_key=self.openai_api_key,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
            )
        gen_ms = (time.time() - t1) * 1000.0
        
        if self.print_prompt:
            print("MODEL RESPONSE:\n" + gen_answer)
            print("=" * 80 + "\n")

        # Map scores by retrieved id (if available) for inclusion
        score_by_id = {}
        try:
            score_by_id = {cid: float(sc) for cid, sc in id_scores}
        except Exception:
            pass

        sources: List[Dict[str, Any]] = []
        for rank, d in enumerate(docs[: self.max_context_docs], start=1):
            md = getattr(d, "metadata", {}) or {}
            chunk_id = (
                self._safe_get(md, "chunk_id")
                or self._safe_get(md, "id")
                or self._safe_get(md, "doc_id")
            )
            score = round(score_by_id.get(chunk_id, 0.0), 3) if chunk_id in score_by_id else None

            preview = (getattr(d, "page_content", "") or "")
            preview = (preview[:240] + "…") if len(preview) > 240 else preview

            src = {
                "rank": rank,
                "score": score,
                "chunk_id": chunk_id,
                "case_id": self._safe_get(md, "case_id"),
                "opinion_id": self._safe_get(md, "opinion_id"),
                "issue": self._safe_get(md, "issue"),
                "court": self._safe_get(md, "court"),
                "year": self._safe_get(md, "year"),
                "text_preview": preview,
            }
            sources.append(src)

        return {
            "answer": gen_answer.strip(),
            "latency_sec": round(time.time() - t_all, 3),
            "timing_ms": {
                "retrieval": round(ret_ms, 1),
                "generation": round(gen_ms, 1),
            },
            "retrieval": {
                "mode": "hybrid",
                "alpha": self.alpha,
                "k": self.k,
                "dense_k": self.dense_k,
                "bm25_k": self.bm25_k,
                "embed_model": self.embed_model,
                "collection": self.collection,
            },
            "model_name": self.model_name,
            "llm_backend": self.backend,
            "sources": sources,
        }
    
if __name__ == "__main__":
    """os.environ.setdefault("LLM_BACKEND", "openai_compatible")
    os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:11434/v1")
    os.environ.setdefault("OPENAI_API_KEY", "ollama")
    
    os.environ.setdefault("DB_DIR", "/Users/innerpiece92/Desktop/Project_Workspace/legal_rag_assistant/lancedb_legal")
    os.environ.setdefault("COLLECTION", "legal_chunks")
    os.environ.setdefault("PROMPT_FILE", "/Users/innerpiece92/Desktop/Project_Workspace/legal_rag_assistant/prompt/prompt_for_legal_assistant_base.txt")

    os.environ.setdefault("MODEL_NAME", "mistral:7b-instruct")
    os.environ.setdefault("DEVICE", "cpu")
    os.environ.setdefault("LOAD_IN_4BIT", "false")
    os.environ.setdefault("MAX_NEW_TOKENS", "256")
    os.environ.setdefault("TEMPERATURE", "0.0")
    os.environ.setdefault("TOP_P", "1.0")

    os.environ.setdefault("K", "50")
    os.environ.setdefault("DENSE_K", "120")
    os.environ.setdefault("BM25_K", "200")
    os.environ.setdefault("ALPHA", "0.6")

    # SCDB flags off unless you provide CODEBOOK_MD_PATH
    os.environ.setdefault("GLOBAL_SCDB", "false")
    os.environ.setdefault("PER_DOC_SCDB", "false")
    os.environ.setdefault("CODEBOOK_MD_PATH", "/Users/innerpiece92/Desktop/Project_Workspace/legal_rag_assistant/llm_ready/SCDB_2023_01_codebook/SCDB_2023_01_codebook.md")
    
    os.environ.setdefault("PRINT_CONTEXT", "true")
    os.environ.setdefault("PRINT_PROMPT", "true")"""

    # Question from CLI
    q = sys.argv[1] if len(sys.argv) > 1 else "Briefly explain the holding in Marbury v. Madison (1803)."

    # Run
    engine = RAGEngine()
    out = engine.answer(q)

    print("\n=== ANSWER ===\n")
    print(out["answer"])

    print("\n=== TIMING (ms) ===")
    print(out["timing_ms"])

    print("\n=== TOP SOURCES ===")
    for s in out["sources"]:
        print(f'[#{s.get("rank")}] score={s.get("score")} year={s.get("year")} court={s.get("court")} id={s.get("chunk_id")}')