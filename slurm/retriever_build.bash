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

# Build (drop --recreate after first run)
# srun -u python retriever.py build ... → cmd_build() → build_lancedb_index(...).
srun -u python retriever.py build \
  --data_path ./tables/chunk.json \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --text_key text_clean \
  --id_key chunk_id \
  --embed_model jinaai/jina-embeddings-v3 \
  --device cuda \
  --recreate

# Single-query (dense)
# srun -u python retriever.py search ... → run_single_query(...)
srun -u python retriever.py search \
  --db_dir ./lancedb_legal \
  --collection legal_chunks \
  --mode dense \
  --k 10 \
  --embed_model jinaai/jina-embeddings-v3 \
  --device cuda \
  --query "What did Justice Scalia say about de novo review in United States v. Arvizu?"