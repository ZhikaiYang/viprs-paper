#!/bin/bash

gwas_software=${1:-"python"}
setup=${2:-"simulation"}

rm -rf "./log/gwas/$gwas_software/" || true
mkdir -p "./log/gwas/$gwas_software"

echo "Submitting jobs for performing GWAS with $gwas_software..."

if [ "$setup" == "simulation" ]; then
  chromosomes=(22)
else
  chromosomes=$(seq 1 22)
fi

for sim_config in data/phenotypes/*
do
  for chr in "${chromosomes[@]}"
    do
    if [ "$gwas_software" == "plink" ]; then
      sbatch -J "plink" gwas/gwas_plink_job.sh "$chr" "$sim_config"
    else
      sbatch -J "python" gwas/gwas_python_job.sh "$chr" "$sim_config"
    fi
  done
done
