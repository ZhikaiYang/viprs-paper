import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Transform summary statistics to PRScs format')

parser.add_argument('-s', '--sumstats', dest='ss_file', type=str, required=True,
                    help='The summary statistics files')
parser.add_argument('-t', '--type', dest='type', type=str, default='plink',
                    choices={'plink', 'pystatgen'})
args = parser.parse_args()

# Read the sumstats file:
ss_df = pd.read_csv(args.ss_file, sep="\t")

if args.type == 'pystatgen':
    ss_df = ss_df[['SNP', 'A1', 'A2', 'BETA', 'PVAL']]
elif args.type == 'plink':
    ss_df = ss_df[['ID', 'ALT1', 'REF', 'BETA', 'P']]

ss_df.columns = ['SNP', 'A1', 'A2', 'BETA', 'P']
ss_df.to_csv(args.ss_file.replace(".PHENO1.glm.linear", ".prscs.ss"), sep="\t", index=False)
