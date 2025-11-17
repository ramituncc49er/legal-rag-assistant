#!/bin/bash
#
#SBATCH --job-name="L_RAG"
#SBATCH --partition=Orion
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=24
#SBATCH --mem=96G
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
module load anaconda3
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate rag_cpu

# Optional scratch caches
export TMPDIR=/scratch/$USER/$SLURM_JOB_ID
mkdir -p "$TMPDIR"
export HF_HOME="$TMPDIR/hf"
export HF_DATASETS_CACHE="$HF_HOME/datasets"
export HF_HUB_CACHE="$HF_HOME/hub"

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export TOKENIZERS_PARALLELISM=false

cd "$SLURM_SUBMIT_DIR"

# ===== Paths (edit these if needed) =====
CASES="tables/cases_master.parquet"
OPINIONS="tables/opinions.parquet"
ISSUES="tables/issues.parquet"
VOTES="tables/votes.parquet"
OUT="tables/documents.parquet"

python corpus_builder.py \
    --cases "$CASES" \
    --opinions "$OPINIONS" \
    --issues "$ISSUES" \
    --votes "$VOTES" \
    --out "$OUT"