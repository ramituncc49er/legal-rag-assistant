#!/bin/bash
#
#SBATCH --job-name="L_RAG"
#SBATCH --partition=Nebula_GPU
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

EXP=legal-rag-main
EVAL=./eval/retrieval_e2e_eval_queries.jsonl
DB=./lancedb_legal
COL=legal_chunks
MODEL=jinaai/jina-embeddings-v3

#for A in 0.4 0.5 0.6 0.7 0.8; do
#  srun -u python retrieval_evaluation.py \
#    --eval_file "$EVAL" \
#    --db_dir "$DB" --collection "$COL" \
#    --embed_model "$MODEL" --device cuda \
#    --mode hybrid --alpha $A --k 80 \
#    --mlflow --mlflow_experiment "$EXP" \
#    --tag_eval_set "hybrid_a${A}_k80"
#done

# Start your alpha, dense_k, bm25_k sweep
for A in 0.4 0.5 0.6; do  # Test different alpha values for hybrid weighting
  for DENSEK in 80 120; do  # Test different dense candidate pool sizes
    for BM25K in 200 400; do  # Test different BM25 candidate pool sizes
      srun -u python retrieval_evaluation.py \
        --eval_file "$EVAL" \
        --db_dir "$DB" --collection "$COL" \
        --embed_model "$MODEL" --device cuda \
        --mode hybrid --alpha $A --k 50 \
        --bm25_k $BM25K --dense_k $DENSEK \
        --mlflow --mlflow_experiment "$EXP" \
        --tag_eval_set "hybrid_a${A}_dense${DENSEK}_bm${BM25K}_k50"
    done
  done
done