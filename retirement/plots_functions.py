import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np
import os

def plot_correlation_matrix(corr_matrix):
    # Plot the correlation matrix
    asset_names = ['US T-Bills', 'US T-Bonds', 'S&P 500', 'Commodities', 'EM Stocks']
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(corr_matrix, square=True, cmap="RdBu_r", annot=True,
                xticklabels=asset_names, yticklabels=asset_names)
    plt.savefig('./outputs/asset_corr_matrix.png', dpi=150)
    plt.close()


def plot_qq_plot(mth_ret, mu, sigma):
    # Examine whether S&P 500 returns exhibit fat tails (Using post World War 2 data)
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.close()
    sm.qqplot(mth_ret.iloc[1:], loc=mu, scale=sigma, fit=True, line='45')
    plt.savefig('./outputs/qq_plot.png', dpi=150)
    plt.close()


def plot_wealth_scenario(ax, perc_df, start_age, N, color, alpha):
    sns.lineplot(x=range(start_age, start_age + N + 1), y=perc_df.columns[0], data=perc_df, color=color, ax=ax)
    sns.lineplot(x=range(start_age, start_age + N + 1), y=perc_df.columns[1], data=perc_df, linewidth=3, ax=ax, label=f'Median Wealth: {np.median(perc_df).round()*1000} (die at {start_age + N})')
    sns.lineplot(x=range(start_age, start_age + N + 1), y=perc_df.columns[2], data=perc_df, color=color, ax=ax)
    sns.lineplot(x=range(start_age, start_age + N + 1), y=1, linewidth=1, color='black', ax=ax)
    ax.fill_between(range(start_age, start_age + N + 1), perc_df[perc_df.columns[0]], perc_df[perc_df.columns[2]],
                    color=color, alpha=alpha, label=f'5th to 95th percentile range (die at {start_age + N})')


def plot_wealth_simulation(perc_df_1, perc_df_2, N, start_age):
    # Plot the wealth over time simulation for two scenarios on the same plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot for the first scenario
    plot_wealth_scenario(ax, perc_df_1, start_age, N, 'lightcyan', 1.0)

    # Plot for the second scenario
    plot_wealth_scenario(ax, perc_df_2, start_age, N, 'lightpink', 0.2)

    ax.set_xlabel("Age", fontsize=16)
    ax.set_ylabel("Wealth ($USD Thousands)", fontsize=16)
    plt.legend(loc='upper left')
    plt.xlim(start_age, start_age + N+5)
    plt.tight_layout()
    plt.savefig('./outputs/port_return.png', dpi=150)
    plt.show()


def plot_wealth_histogram(wealths_1, spend_1, wealths_2, spend_2):
    # Histogram that shows the distribution of the Monte Carlo Results for 2 spending levels
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.histplot(wealths_1.loc[30], kde=False, bins=120, label=f'Spending=${spend_1},000')
    sns.histplot(wealths_2.loc[30], kde=False, bins=120, label=f'Spending=${spend_2},000', color='pink')
    plt.axvline(x=0, color='red')
    plt.xlim(-1500, 2000)

    ax.set_xlabel("Wealth at Age 85 ($USD Thousands)", fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    plt.legend()
    plt.tight_layout()

    plt.savefig('./outputs/port_hist.png', dpi=150)
    plt.show()
