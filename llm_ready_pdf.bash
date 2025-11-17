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

### === User params ===
INPUT="/users/raditya/raditya_workspace/rag_assistant/SCDB_2023_01_codebook.pdf"
OUTDIR="/users/raditya/raditya_workspace/rag_assistant/llm_ready"             # output root
PARQUET_MODE="chunks"                          # "single" or "chunks"
CHUNK=1800                                     # chars per chunk when PARQUET_MODE=chunks

module load anaconda3
mkdir -p logs

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

# Make sure output dir exists
mkdir -p "$OUTDIR"

python llm_ready_pdf.py \
  --input "$INPUT" \
  --out "$OUTDIR" \
  --parquet "$PARQUET_MODE" \
  --chunk $CHUNK