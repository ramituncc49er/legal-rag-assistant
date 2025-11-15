"""
config.py
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def set_default_env():
    """
    Set default environment variables for the Legal RAG Assistant.
    Uses os.environ.setdefault so shell overrides still win.
    """
    # ================== LLM backend / API ==================
    os.environ.setdefault("LLM_BACKEND", "openai_compatible")   # or "transformers"
    os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:11434/v1")
    os.environ.setdefault("OPENAI_API_KEY", "ollama")

    # ================== Retrieval ==================
    os.environ.setdefault("DB_DIR", os.path.join(PROJECT_ROOT, "lancedb_legal"))
    os.environ.setdefault("COLLECTION", "legal_chunks")

    # ================== Prompt ==================
    os.environ.setdefault(
        "PROMPT_FILE",
        os.path.join(
            PROJECT_ROOT,
            "prompt",
            "prompt_for_legal_assistant_base.txt",
        ),
    )
    os.environ.setdefault(
        "CODEBOOK_MD_PATH",
        os.path.join(
            PROJECT_ROOT,
            "llm_ready",
            "SCDB_2023_01_codebook",
            "SCDB_2023_01_codebook.md",
        ),
    )

    # ================== Model ==================
    os.environ.setdefault("MODEL_NAME", "mistral:7b-instruct")  # Ollama model name
    os.environ.setdefault("DEVICE", "cpu")
    os.environ.setdefault("LOAD_IN_4BIT", "false")
    os.environ.setdefault("LOAD_IN_8BIT", "false")
    os.environ.setdefault("DTYPE", "float16")
    os.environ.setdefault("MAX_NEW_TOKENS", "256")
    os.environ.setdefault("TEMPERATURE", "0.0")  # deterministic for demo
    os.environ.setdefault("TOP_P", "1.0")

    # ================== Retrieval knobs ==================
    os.environ.setdefault("K", "50")
    os.environ.setdefault("DENSE_K", "120")
    os.environ.setdefault("BM25_K", "200")
    os.environ.setdefault("ALPHA", "0.6")

    # ================== Context ==================
    os.environ.setdefault("MAX_CONTEXT_DOCS", "8")
    os.environ.setdefault("STRIP_META", "false")
    os.environ.setdefault("META_MAX_VALUE_CHARS", "200")
    os.environ.setdefault("GLOBAL_SCDB", "false")
    os.environ.setdefault("PER_DOC_SCDB", "false")

    # ================== Debug ==================
    os.environ.setdefault("PRINT_CONTEXT", "false")
    os.environ.setdefault("PRINT_PROMPT", "false")

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
