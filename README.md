# Legal RAG Assistant
This repository contains source code for a RAG-based LLM assistant for U.S. Supreme Court case law built on CourtListener and SCDB data.

Key features:
- Built using subset of the **CourtListener dataset (4.6M+ records)**, selecting only U.S. Supreme Court cases and matching them with SCDB metadata.
- Dense + BM25 hybrid retrieval using LanceDB to index Supreme Court opinions.
- Domain-specific prompt templates tailored for question answering and citation.
- End-to-end system: ingestion → chunking → embedding → retrieval → LLM inference → evaluation.

<p align="center">
  <img src="figs/Legal_RAG_Assistant.png" height="600">
</p>

# Dataset

- Courtlistner: [https://huggingface.co/datasets/wildphoton/courtlistener_opinions](https://huggingface.co/datasets/wildphoton/courtlistener_opinions)
- Supreme Court Database: [http://scdb.wustl.edu/data.php](http://scdb.wustl.edu/data.php)

## Repository Structure

```text
legal_rag_assistant/
├─src/
│ ├─ app.py               # Streamlit interactive demo of the assistant
│ ├─ config.py            # Configuration / environment variable handling
│ ├─ rag_engine.py        # Core RAG engine (retriever + generator)
│ ├─ retriever.py         # Retrieval logic: dense, BM25, hybrid
│ ├─ inference.py         # LLM prompt templates and generation logic
│ ├─ retrieval_eval.py    # Retrieval-only evaluation CLI
│ ├─ e2e_eval.py          # End-to-end evaluation
│ ├─ data_pipeline.py     # Raw data ingestion and preprocessing pipeline
│ ├─ chunk_builder.py     # Chunking logic for opinions/cases
│ ├─ corpus_builder.py    # Corpus assembly from raw CourtListener + SCDB data
│ ├─ ingest.py            # Scripts to ingest into LanceDB
│
├─ llm_ready/             # “LLM-readable” SCDB Codebook using 'marker' for context augumentation
├─ prompt/                # Directory: prompt templates & system messages
├─ eval/                  # Directory: evaluation config files + scripts
├─ slurm/                 # HPC job scripts (Slurm) for index build & evaluation
│
├─ README.md
├─ LICENSE
└─ .gitignore             # Ignore rules for repo
```

The LanceDB index is stored locally under `lancedb_legal/` (gitignored).
Scripts to build it from the SCDB + CourtListener data will be added under `src/`

## Environment Setup

- Install Python 3.11+ and set up a virtual environment.
- Install PyTorch with CUDA support.
- Install all dependencies: `pip install -r requirements.txt`

## Models Used

The Streamlit app uses **Mistral 7B Instruct** served locally through **Ollama**.

- **Model:** `mistral:7b-instruct`
- **Provider:** [Ollama](https://ollama.com/)

### Setting up Mistral in Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh          # Install Ollama
ollama pull mistral:7b-instruct                        # Pull the model
ollama run mistral:7b-instruct                         # Verify the model
```

## Roadmap / TODO

This is an early building block toward a long-term vision:  **an AI-augmented legal assistant capable of reducing the time and cognitive load involved in complex written legal processes.**

### AI Legal Assistant (Long-Term Vision)

- [ ] Automated drafting of:
  - case summaries and digests  
  - issue-specific briefs and memos  
  - comparative case overviews (e.g., “how have courts treated X across circuits”)
- [ ] Automatic extraction of:
  - parties, claims, issues, holdings  
  - procedural posture (trial, appeal, remand, etc.)
  - legal tests and standards used in a decision
- [ ] Semi-structured outputs to feed into downstream tools:
  - tables of authorities  
  - checklists for compliance or risk review  
  - structured JSON/CSV exports for further analysis
- [ ] Workflows to support:
  - document review  
  - knowledge-base curation  
  - drafting “first versions” that humans can refine
     
## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
