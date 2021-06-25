import os.path as osp
import sys
sys.path.append(osp.dirname(osp.dirname(__file__)))
from utils import makedir
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import functools
print = functools.partial(print, flush=True)


print("> Plotting time statistics for PRS methods...")

time_df = []

# Loop over the log files and extract the duration for each run
# as well as associated info (e.g. configuration, model, LD panel, etc.):
for log_f in glob.glob("log/model_fit/*/*/*/*.out"):

    _, _, panel, model, config, _ = log_f.split('/')

    try:
        with open(log_f, 'r') as f:
            lines = f.read().splitlines()
            duration = float(lines[-1].split(':')[-1].strip())
            trait, chrom = lines[2].split("/")[-2:]
            chrom = chrom.replace("chr_", "").replace(".PHENO1.glm.linear", "")

        time_df.append({'LD Panel': panel,
                        'Configuration': config,
                        'Chromosome': int(chrom),
                        'Trait': trait,
                        'Model': model,
                        'Duration': duration})

    except Exception as e:
        print(e)
        continue

# Concatenate the entries into a single dataframe:
time_df = pd.DataFrame(time_df)

# ---------------------------------------------------------
# Plot 1: Plot time statistics for simulations by LD panel:

print("> Plotting time statistics by LD panel for simulations...")

ldp_time_df = time_df.loc[time_df['Configuration'] != 'real'].groupby(
    ['LD Panel', 'Configuration', 'Trait', 'Model']
).sum()

for ldp in ldp_time_df['LD Panel'].unique():

    if ldp == 'external':
        continue

    df = ldp_time_df.loc[ldp_time_df['LD Panel'].isin(['external', ldp])]

    plt.figure(figsize=(9, 6))
    ax = sns.boxplot(x="Model", y="Duration", hue="Model", data=df)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.ylabel("Runtime (Minutes)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    makedir(f"plots/runtime_stats/ld_panel/{ldp}")

    plt.savefig(f"plots/runtime_stats/ld_panel/{ldp}/simulation_runtime.pdf", bbox_inches='tight')
    plt.close()

# ---------------------------------------------------------
# Plot 2: Plot time statistics for real data by LD panel:

print("> Plotting time statistics by LD panel for real data...")

ldp_time_df = time_df.loc[time_df['Configuration'] == 'real'].groupby(
    ['LD Panel', 'Configuration', 'Trait', 'Model']
).sum()

for ldp in ldp_time_df['LD Panel'].unique():

    if ldp == 'external':
        continue

    df = ldp_time_df.loc[ldp_time_df['LD Panel'].isin(['external', ldp])]

    plt.figure(figsize=(9, 6))
    ax = sns.boxplot(x="Model", y="Duration", hue="Model", data=df)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.ylabel("Runtime (Minutes)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(f"plots/runtime_stats/ld_panel/{ldp}/real_runtime.pdf", bbox_inches='tight')
    plt.close()

# ---------------------------------------------------------
# Plots 3: Plot time statistics by chromosome:

print("> Plotting time statistics by chromosome...")

plt.figure(figsize=(9, 6))
ax = sns.boxplot(x="Chromosome", y="Duration", hue="Model", data=time_df)
plt.ylabel("Runtime (Minutes)")
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig(f"plots/runtime_stats/chromosome_runtime.pdf", bbox_inches='tight')
plt.close()
