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

# ===== Paths =====
DOCS="tables/documents.parquet"
OUTDIR="tables"   # chunk_builder.py writes OUTDIR/chunk.json

# ===== Parameters (override with: sbatch --export=ALL,ROW_INDEX=...,START_INDEX=...,NUM_RECORDS=...) =====
#ROW_INDEX=1              # set to a number to process a single row (e.g., 123)
START_INDEX=0
NUM_RECORDS=-1             # -1 = all from START_INDEX
MAX_TOKENS=900
OVERLAP_TOKENS=180
SENTENCE_SPLIT_THRESHOLD=1300
MAX_PARAS_PER_CHUNK=12
MAX_CHARS_PER_CHUNK=8000
TEXT_COLS="opinion_text"

# ===== Build CLI =====
ARGS=(
  --docs "$DOCS"
  --out "$OUTDIR"
  --text-cols "$TEXT_COLS"
  --max-tokens "$MAX_TOKENS"
  --overlap-tokens "$OVERLAP_TOKENS"
  --sentence-split-threshold "$SENTENCE_SPLIT_THRESHOLD"
  --max-paragraphs-per-chunk "$MAX_PARAS_PER_CHUNK"
  --max-chunk-chars "$MAX_CHARS_PER_CHUNK"
  --start-index "$START_INDEX"
  --num-records "$NUM_RECORDS"
)

python chunk_builder.py "${ARGS[@]}"