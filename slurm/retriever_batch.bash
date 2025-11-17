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
# Log locally to ./mlruns (view later via: mlflow ui --backend-store-uri ./mlruns)
export MLFLOW_TRACKING_URI=./mlruns
echo "CUDA available?"; python - <<'PY'
import torch; print(torch.cuda.is_available())
PY
nvidia-smi || true

# Batch run: logs p50/p95 to MLflow
srun -u python retriever.py batch \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --mode hybrid \
  --alpha 0.6 \
  --bm25_k 40 \
  --dense_k 40 \
  --k 20 \
  --embed_model jinaai/jina-embeddings-v3 \
  --device cuda \
  --queries_file ./eval/retrieval_eval_queries.txt \
  --mlflow_exp legal-rag-main \
  --mlflow_run_tag phase=1