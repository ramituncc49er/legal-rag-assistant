#!/bin/bash
#
#SBATCH --job-name="L_RAG"
#SBATCH --partition=GPU
#SBATCH --time=04:00:00
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
echo "CUDA available?"; python - <<'PY'
import torch; print(torch.cuda.is_available())
PY
nvidia-smi || true

# Hybrid + CrossEncoder rerank top-20 → return top-10
srun -u python retriever.py search \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --mode hybrid \
  --alpha 0.6 \
  --bm25_k 40 \
  --dense_k 40 \
  --k 10 \
  --embed_model jinaai/jina-embeddings-v3 \
  --reranker cross-encoder/ms-marco-MiniLM-L-6-v2 \
  --rerank_top_n 20 \
  --device cuda \
  --query "What did Justice Scalia say about de novo review in United States v. Arvizu?"