"""
This script generates plots for the fifth figure in the manuscript
where we show predictive performance on real quantitative
phenotypes using up to 10 million variants.
"""

from plot_predictive_performance import *

parser = argparse.ArgumentParser(description='Generate Figure 5')
parser.add_argument('--extension', dest='ext', type=str, default='eps')
args = parser.parse_args()


def extract_lines(data_df, metric='R2',
                  reference_model=None, reference_color='black',
                  add_best_model=True, best_model_color='red'):

    lines = []

    if reference_model is not None:
        # Extract data for the reference model:
        values = data_df.loc[data_df.Model == reference_model].groupby('Trait')[metric].mean().to_dict()
        lines.append({'values': values, 'color': reference_color, 'label': reference_model + ' (HapMap3)'})

    # Extract data for the best model:
    if add_best_model:
        best_m_df = data_df.groupby(['Trait', 'Model']).mean().sort_values(
            ['Trait', metric], axis=0
        ).groupby(['Trait']).tail(1)[metric]
        best_m_df.index = best_m_df.index.get_level_values('Trait')

        values = best_m_df.to_dict()

        lines.append({'values': values, 'color': best_model_color, 'label': 'Best model (HapMap3)'})

    return lines


# Extract data:
keep_panels = ['ukbb_50k_windowed', 'external']


quant_real_data = extract_predictive_evaluation_data(phenotype_type='quantitative',
                                                     configuration='real',
                                                     keep_models=['VIPRS', 'VIPRS-GSv_p', 'SBayesR'],
                                                     keep_panels=keep_panels,
                                                     keep_traits=['HEIGHT', 'HDL', 'BMI',
                                                                  'FVC', 'FEV1', 'HC',
                                                                  'WC', 'LDL', 'BW']
                                                     )
quant_real_data = update_model_names(quant_real_data)
quant_real_data['Model'] = quant_real_data['Model'].map({'VIPRS': 'VIPRS (HapMap3)',
                                                         'VIPRS-GS': 'VIPRS-GS (HapMap3)'})

quant_real_10m = extract_predictive_evaluation_data(phenotype_type='quantitative',
                                                    keep_models=['VIPRS', 'VIPRS-GSp_p'],
                                                    configuration='real',
                                                    keep_traits=['HEIGHT', 'HDL', 'BMI',
                                                                 'FVC', 'FEV1', 'HC',
                                                                 'WC', 'LDL', 'BW'],
                                                    eval_dir="data_all/evaluation")

quant_real_10m['Model'] = quant_real_10m['Model'].map({'VIPRS': 'VIPRS-10m',
                                                       'VIPRS-GSp_p': 'VIPRS-GS-10m'})

quant_real_data = pd.concat([quant_real_data, quant_real_10m])

# Set seaborn context:
makedir("plots/main_figures/figure_5/")
sns.set_style("darkgrid")

"""
sns.set_context("paper", font_scale=1.2)

# Create plot:

# version 1:
plt.figure(figsize=set_figure_size(width='paper'))

lines = extract_lines(quant_real_data.loc[~quant_real_data.Model.isin(['VIPRS-10m', 'VIPRS-GS-10m']),],
                      reference_model='VIPRS')

plot_real_predictive_performance_with_lines(quant_real_data,
                                            lines=lines,
                                            trait_order=sort_traits('quantitative', quant_real_data['Trait'].unique()),
                                            model_order=['VIPRS-10m', 'VIPRS-GS-10m'],
                                            palette=['#66c2a5', '#fc8d62'])
plt.savefig("plots/main_figures/figure_5/5." + args.ext, bbox_inches='tight')
plt.close()
"""

# version 2:
sns.set_context("paper", font_scale=1.2)
plt.figure(figsize=set_figure_size(width='paper', width_extra_pct=.5))

lines = extract_lines(quant_real_data.loc[~quant_real_data.Model.isin(['VIPRS-10m', 'VIPRS-GS-10m']),])

plot_real_predictive_performance_with_lines(quant_real_data,
                                            lines=None, #lines,
                                            trait_order=sort_traits('quantitative', quant_real_data['Trait'].unique()),
                                            model_order=['VIPRS (HapMap3)', 'VIPRS-10m',
                                                         'VIPRS-GS (HapMap3)', 'VIPRS-GS-10m'],
                                            palette=['#c4d7d1', '#5f9595', '#f5d1c3', '#ffb7a1'])
plt.savefig("plots/main_figures/figure_5/5." + args.ext, bbox_inches='tight')
plt.close()

"""
# version 3:

plt.figure(figsize=set_figure_size(width='paper'))

plot_real_predictive_performance_with_lines(quant_real_data,
                                            lines=lines,
                                            trait_order=sort_traits('quantitative', quant_real_data['Trait'].unique()),
                                            model_order=['VIPRS-GS', 'VIPRS-GS-10m'],
                                            palette=['#fc8d62', '#854b34'])
plt.savefig("plots/main_figures/figure_5/5_v3." + args.ext, bbox_inches='tight')
plt.close()
"""

"""
plt.figure(figsize=set_figure_size(width=.75*505.89, subplots=(3, 3)))

plot_real_predictive_performance(quant_real_data,
                                 model_order=['VIPRS', 'VIPRSMix',
                                              'VIPRS-10m', 'VIPRSMix-10m',
                                              'VIPRS-GS', 'SBayesR'],
                                 row_order=sort_traits('quantitative', quant_real_data['Trait'].unique()),
                                 col_order=sort_traits('quantitative', quant_real_data['Trait'].unique()),
                                 col_wrap=3,
                                 palette=['#b2df8a', '#33a02c', '#a6cee3', '#1f78b4', '#fc8d62', '#cab2d6'])
plt.subplots_adjust(wspace=.1)
plt.savefig("plots/main_figures/figure_5/5_a." + args.ext, bbox_inches='tight')
plt.close()


plt.figure(figsize=set_figure_size(width=.25*505.89, subplots=(3, 1)))

plot_real_predictive_performance(bin_real_data,
                                 metric='PR-AUC',
                                 model_order=['VIPRS', 'VIPRSMix',
                                              'VIPRS-10m', 'VIPRSMix-10m',
                                              'VIPRS-GS', 'SBayesR'],
                                 row_order=sort_traits('binary', bin_real_data['Trait'].unique()),
                                 col_wrap=1,
                                 palette=['#b2df8a', '#33a02c', '#a6cee3', '#1f78b4', '#fc8d62', '#cab2d6'])
plt.subplots_adjust(wspace=.1)
plt.savefig("plots/main_figures/figure_5/5_b." + args.ext, bbox_inches='tight')
plt.close()

plt.figure(figsize=set_figure_size(width='paper'))

plot_real_predictive_performance_relative_improvement(quant_real_data,
                                                      metric='R2',
                                                      trait_order=sort_traits('quantitative', quant_real_data['Trait'].unique()),
                                                      model_order=['VIPRS-10m', 'VIPRSMix-10m'],
                                                      palette=['#fc8d62', '#cab2d6'])
plt.savefig("plots/main_figures/figure_5/5_d." + args.ext, bbox_inches='tight')
plt.close()
"""

