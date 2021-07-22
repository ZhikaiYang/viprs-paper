#!/bin/bash
#SBATCH --account=def-sgravel
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=2GB
#SBATCH --time=2:00:00
#SBATCH --output=./log/simulation/%j.out
#SBATCH --mail-user=shadi.zabad@mail.mcgill.ca
#SBATCH --mail-type=FAIL

source "$HOME/pyenv/bin/activate"
module load plink

H2G=${1:-0.1}  # Heritability (default 0.1)
PC=${2:-0.01}  # Proportion of causal variants (default 0.01)
NREP=${3:-10}  # Number of replicates (default 10)

echo "Performing phenotype simulation using the following configurations:"
echo "Heritability: $H2G"
echo "Proportion of causal variants: $PC"
echo "Number of replicates: $NREP"

parallel -j 4 python simulation/simulate_phenotypes.py --h2g "$H2G" -p "$PC" -r {} ::: $(seq 1 $NREP)

echo "Job finished with exit code $? at: `date`"
