"""
app.py

- Streamlit app (app.py): UI + calls RAGEngine().answer(question)
- RAGEngine (rag_engine.py): retrieval + prompt building + LLM call (Ollama via openai-compatible API).
- Ollama: Separate local HTTP service.
"""
import os
import time
import streamlit as st

from config import set_default_env
from rag_engine import RAGEngine

set_default_env()


@st.cache_resource(show_spinner=True)
def load_engine(model_name: str):
    """
    Construct a RAGEngine once per model_name.
    We fix the backend to 'openai_compatible' (Ollama).
    """
    os.environ["MODEL_NAME"] = model_name
    os.environ["LLM_BACKEND"] = "openai_compatible"
    return RAGEngine()


def main():
    st.set_page_config(page_title="Legal RAG Assistant Demo", layout="wide")

    st.title("Legal RAG Assistant")
    st.write(
        "Ask a question about U.S. Supreme Court cases.\n\n"
        "Example: *Which employees did the Interstate Commerce Commission find subject to its "
        "authority under section 204(a) of the Motor Carrier Act?*"
    )

    # Sidebar controls
    with st.sidebar:
        st.header("Settings")

        # Backend is fixed to Ollama-style openai-compatible
        backend = "openai_compatible"
        st.write(f"**LLM backend:** `{backend}`")

        # Model selector (Ollama models)
        model_options = [
            "mistral:7b-instruct",
            #"gemma3:12b",
        ]
        current_model = os.getenv("MODEL_NAME", model_options[0])
        model_name = st.selectbox(
            "Model",
            model_options,
            index=model_options.index(current_model) if current_model in model_options else 0,
        )
        st.write(f"**Selected model:** `{model_name}`")

        # Temperature / max tokens
        temperature = st.slider(
            "Temperature",
            0.0, 1.0,
            float(os.getenv("TEMPERATURE", "0.0")),
            0.1,
        )
        max_new_tokens = st.slider(
            "Max new tokens",
            64, 512,
            int(os.getenv("MAX_NEW_TOKENS", "256")),
            32,
        )

        # Push updated values into env for RAGEngine
        os.environ["TEMPERATURE"] = str(temperature)
        os.environ["MAX_NEW_TOKENS"] = str(max_new_tokens)

        st.caption(
            "If you change the model, the app will spin up (and cache) a separate engine instance for that model."
        )

    # Main input
    question = st.text_area(
        "Enter your question:",
        value="",
        height=120,
        placeholder="e.g., Which employees did the Interstate Commerce Commission find subject to its authority "
                    "under section 204(a) of the Motor Carrier Act?",
    )

    if st.button("Run RAG", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        # Build / fetch cached engine for the selected model
        engine = load_engine(model_name)

        with st.spinner("Retrieving documents and generating answer..."):
            t0 = time.time()
            result = engine.answer(question.strip())
            total_ms = (time.time() - t0) * 1000.0

        # Answer block
        st.subheader("Answer")
        st.write(result["answer"])

        # Timing
        st.subheader("Timing")
        st.json({
            "retrieval_ms": result["timing_ms"]["retrieval"],
            "generation_ms": result["timing_ms"]["generation"],
            "total_ms": round(total_ms, 1),
        })

        # Sources
        st.subheader("Sources (Top retrieved chunks)")
        sources = result.get("sources", [])
        if not sources:
            st.info("No sources returned.")
        else:
            import pandas as pd

            df = pd.DataFrame(sources)
            cols = ["rank", "score", "chunk_id", "case_id", "opinion_id", "issue", "court", "year", "text_preview"]
            cols = [c for c in cols if c in df.columns]
            st.dataframe(df[cols], use_container_width=True)

        # Debug
        with st.expander("Raw JSON output (for debugging)"):
            st.json(result)


if __name__ == "__main__":
    main()