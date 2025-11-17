#!/bin/bash
#
#SBATCH --job-name="L_RAG"
#SBATCH --partition=GPU
# #SBATCH --partition=Nebula_GPU
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --mem=96G
# #SBATCH --output=rag_smoke_%j.out
# #SBATCH --constraint=xeon
#
#   ===== Main =====
                                                                                                                                                                      
# #                                                                                                                                                                                                 
# #To activate this environment, use                                                                                                                                                                 
# #                                                                                                                                                                                                  
# #    $ conda activate rag_cpu                                                                                                                                                                      
# #                                                                                                                                                                                                  
# #To deactivate an active environment, use                                                                                                                                                          
# #                                                                                                                                                                                                  
# #    $ conda deactivate                                                                                                                                                                            
# #
module load pytorch/2.3.0-cuda12.1
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate rag_cpu

# Optional scratch caches
export HF_HOME=${SLURM_TMPDIR:-/tmp}/.cache/huggingface
# export TRANSFORMERS_CACHE=$HF_HOME
export TOKENIZERS_PARALLELISM=false
export HUGGING_FACE_HUB_TOKEN="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"
echo "CUDA available?"; python - <<'PY'
import torch; print(torch.cuda.is_available())
PY
nvidia-smi || true

#   ===== Model inference run =====
# --model_name mistralai/Mistral-7B-Instruct-v0.3 \
# --model_name meta-llama/Meta-Llama-3-8B-Instruct \
# --model_name deepseek-ai/deepseek-coder-6.7b-instruct \
# --model_name Qwen/Qwen3-4B-Instruct-2507 \

srun -u python inference.py \
  --queries_file ./eval/retrieval_e2e_eval_queries.jsonl \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --embed_model jinaai/jina-embeddings-v3 \
  --device cuda \
  --model_name Qwen/Qwen3-4B-Instruct-2507 \
  --codebook_md_path ./llm_ready/SCDB_2023_01_codebook/SCDB_2023_01_codebook.md \
  --prompt_file ./prompt/prompt_for_legal_assistant_base.txt \
  --out_jsonl ./model_response/inference_results_qwen3.jsonl \
  --k 50 --alpha 0.6 --dense_k 120 --bm25_k 200 \
  --max_context_docs 8 \
  --print_prompt \
  --verbose