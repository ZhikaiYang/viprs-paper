import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Transform summary statistics to MegaPRS format')

parser.add_argument('-s', '--sumstats', dest='ss_file', type=str, required=True,
                    help='The summary statistics files')
parser.add_argument('-t', '--type', dest='type', type=str, default='plink',
                    choices={'plink', 'magenpy'})
args = parser.parse_args()

print(f"> Transforming summary statistics file: {args.ss_file}")
# Read the sumstats file:
ss_df = pd.read_csv(args.ss_file, sep="\t")

if args.type == 'magenpy':
    ss_df = ss_df[['SNP', 'A1', 'A2', 'N', 'Z']]
elif args.type == 'plink':
    ss_df['A2'] = ss_df.apply(lambda x: [x['ALT1'], x['REF']][x['A1'] == x['ALT1']], axis=1)
    try:
        ss_df = ss_df[['ID', 'A1', 'A2', 'OBS_CT', 'T_STAT']]
    except KeyError:
        ss_df = ss_df[['ID', 'A1', 'A2', 'OBS_CT', 'Z_STAT']]

ss_df.columns = ['Predictor', 'A1', 'A2', 'n', 'Z']

if 'linear' in args.ss_file:
    new_f_name = args.ss_file.replace(".PHENO1.glm.linear", ".megaprs.ss")
else:
    new_f_name = args.ss_file.replace(".PHENO1.glm.logistic", ".megaprs.ss")

ss_df.to_csv(new_f_name, sep="\t", index=False)
