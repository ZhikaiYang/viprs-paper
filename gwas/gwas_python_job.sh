#!/bin/bash
#SBATCH --account=def-sgravel
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=8GB
#SBATCH --time=01:00:00
#SBATCH --output=./log/gwas/%x/%j.out
#SBATCH --mail-user=shadi.zabad@mail.mcgill.ca
#SBATCH --mail-type=FAIL

source "$HOME/pyenv/bin/activate"

python gwas/python_gwas.py -i "$1"

echo "Job finished with exit code $? at: `date`"
