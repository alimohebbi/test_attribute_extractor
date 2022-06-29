import re
from os import listdir

from matplotlib.lines import Line2D
from scipy.stats import ttest_1samp, stats

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sn
from sklearn import preprocessing

from analyse import Analyse
from util import rename_subjects, make_config_column, add_mig_name, add_unified_mig_name, add_file_name_as_config


def get_concat_result(path):
    results_fname = [f for f in listdir(path) if '.csv' in f]
    all_results = []
    for fname in results_fname:
        result_f = pd.read_csv(path + fname)
        add_file_name_as_config(result_f, fname)
        all_results.append(result_f)
    all_results_df = pd.concat(all_results)
    all_results_df = all_results_df[['src_app', 'target_app', 'f1_score', 'config']]
    return all_results_df.sort_values(by=['src_app', 'target_app'])


def describe_f1_per_migration(all_results_df, save_path):
    groups_by = ['src_app', 'target_app']
    grouped_results = all_results_df.groupby(by=groups_by)
    group_desc = grouped_results['f1_score'].describe()
    group_desc.to_csv(save_path)


def creat_box_plots(df, column, save_path):
    plt.clf()
    plt.close()
    plt.figure(figsize=(20, 5))
    add_mig_name(df)

    ax = sn.boxplot(data=df, y=column, x='mig_name')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    sn.stripplot(data=df, y=column, x='mig_name', jitter=True,
                 dodge=True,
                 marker='o',
                 alpha=0.5)
    plt.savefig(save_path, bbox_inches='tight')


def get_tool_type(x):
    return 'craft' if bool(re.search('a[6-8]', x['src_app'])) else 'atm'


def creat_box_plots_sbs(df, column, save_path):
    plt.clf()
    plt.close()
    plt.figure(figsize=(20, 5))
    if 'task' not in df.columns:
        df['task'] = ''
    df['mig_name'] = df['src_app'] + ' - ' + df['target_app'] + ' - ' + df['task']
    df['tool'] = ''
    df['tool'] = df.apply(get_tool_type, axis=1)
    df['mig_name'] = df.apply(rename_subjects, axis=1)
    ax = sn.boxplot(data=df, y=column, x='mig_name', hue='tool')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    sn.stripplot(data=df, y=column, x='mig_name', hue='tool', jitter=True,
                 dodge=True,
                 marker='o',
                 alpha=0.5)
    plt.savefig(save_path, bbox_inches='tight')


def prepare_df_for_config_frange(df):
    df = normalize_delta(df.copy().fillna(0))
    df = make_config_column(df.fillna(0))
    # df = df[~df['config'].str.contains('random')]
    add_unified_mig_name(df)
    df.drop(columns=['src_app', 'target_app', 'task'], inplace=True)
    return df


def config_normalization(df):
    df1_grouped = df.groupby('config')
    dfs = []
    for group_name, df_group in df1_grouped:
        df_group = normalize_delta(df_group)
        dfs.append(df_group)
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df = make_config_column(df)
    return df


def normalize_delta(df):
    x = df['f1_score'].values
    standard_scaler = preprocessing.StandardScaler(with_std=False)
    x_scaled = standard_scaler.fit_transform(x.reshape(-1, 1))
    df['f1_score'] = x_scaled
    return df


def agg_atm_random_configs(atm_atm_df):
    result = atm_atm_df.groupby(by=['config', 'mig_name'], as_index=False).agg("mean")
    return result


def config_delta_per_mig(atm_atm_df: pd.DataFrame, craft_atm_df: pd.DataFrame):
    atm_atm_df = prepare_df_for_config_frange(atm_atm_df)
    craft_atm_df = prepare_df_for_config_frange(craft_atm_df)
    atm_atm_df = agg_atm_random_configs(atm_atm_df)
    joined_dfs = pd.merge(atm_atm_df, craft_atm_df, how='inner', on=["config", "mig_name"], suffixes=("_atm", "_craft"))
    joined_dfs['delta'] = joined_dfs['F1 score_atm'] - joined_dfs['F1 score_craft']
    creat_delta_box_plots(joined_dfs)


def get_palette(data):
    palette = {}
    configs = data['config'].unique()
    for conf in configs:
        sample = data[data['config'] == conf]
        tscore, pvalue = ttest_1samp(sample['delta'], popmean=0.0)
        if pvalue / 2 < 0.05 and tscore < 0:  # one tailed ttest
            palette[conf] = 'tab:orange'
        elif pvalue / 2 < 0.05 and tscore > 0:
            palette[conf] = 'tab:blue'
        else:
            palette[conf] = 'lavender'
    return palette


def creat_delta_box_plots(df):
    plt.clf()
    plt.close()
    plt.figure(figsize=(20, 5))
    plt.ylim((-1, 1))
    order = df.groupby(by=["config"])["delta"].mean().sort_values(ascending=True).index
    palette = get_palette(df)
    ax = sn.boxplot(data=df, y='delta', x='config', order=order, palette=palette, showmeans=True,
                    meanprops=Analyse.get_mean_props())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    add_legend()
    plt.savefig('delta/delta.pdf', bbox_inches='tight')


def add_legend():
    custom_lines = [Line2D([0], [0], color='lavender', lw=4),
                    Line2D([0], [0], color='tab:blue', lw=4),
                    Line2D([0], [0], color='tab:orange', lw=4),
                    Line2D([0], [0], marker="^", markeredgecolor="green", markerfacecolor='red', markersize="7", lw=0)
                    ]
    plt.legend(custom_lines, ['Indifference', 'ATM benefited', 'CrafDroid benefited', 'Mean'])


if __name__ == '__main__':
    path = '../data/output/evaluation/atm/oracles_included/without_oracle_pass/'
    atm_df = get_concat_result(path)
    # describe_f1_per_migration(atm_df, 'f1_range/table/atm.csv')
    # creat_box_plots(atm_df, 'f1_score', 'f1_range/plots/atm_f1_range.pdf')
    #
    path = '../data/output/evaluation/craftdroid/oracles_included/'
    all_results_df = get_concat_result(path)
    # describe_f1_per_migration(all_results_df, 'f1_range/table/craft_all.csv')
    # creat_box_plots(all_results_df, 'f1_score', 'f1_range/plots/craft_all_f1_range.pdf')
    #
    # craft_craft_df = all_results_df[~all_results_df['src_app'].str.contains('a6|a7|a8')]
    # describe_f1_per_migration(craft_craft_df, 'f1_range/table/craft_craft.csv')
    # creat_box_plots(craft_craft_df, 'f1_score', 'f1_range/plots/craft_craft_f1_range.pdf')
    #
    craft_atm_df = all_results_df[all_results_df['src_app'].str.contains('a6|a7|a8')]
    # describe_f1_per_migration(craft_atm_df, 'f1_range/table/craft_atm.csv')
    # creat_box_plots(craft_atm_df, 'f1_score', 'f1_range/plots/craft_atm_f1_range.pdf')
    #
    # side_by_side_df = pd.concat([atm_df, craft_atm_df])
    # creat_box_plots_sbs(side_by_side_df, 'f1_score', 'f1_range/plots/craft_sbs_f1_range.pdf')
    config_delta_per_mig(atm_df, craft_atm_df)
