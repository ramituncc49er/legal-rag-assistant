#!/bin/bash
#
#SBATCH --job-name="L_RAG"
# #SBATCH --partition=GPU
#SBATCH --partition=Nebula_GPU
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
echo "CUDA available?"; python - <<'PY'
import torch; print(torch.cuda.is_available())
PY
nvidia-smi || true

srun -u python e2e_eval.py \
  --queries_file ./eval/retrieval_e2e_eval_queries.jsonl \
  --inference_results ./model_response/inference_results_qwen3.jsonl \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --embed_model jinaai/jina-embeddings-v3 \
  --recompute_context \
  --verbose