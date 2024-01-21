import pandas as pd
import numpy as np
import random
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
from compute_gains import calculate_outflows

# set the numpy random seed to allow replication of results
np.random.seed(seed=7)


# Set the backend to inline if using IPython or Jupyter
# This is not strictly necessary in a script, but can be included for compatibility
try:
    from IPython import get_ipython
    if get_ipython():
        get_ipython().run_line_magic('matplotlib', 'inline')
except ImportError:
    pass


# Set the figure size
plt.rcParams['figure.figsize'] = (12, 6)

def plot_subplot(data, config):
    plt.plot(data, label=config['label'])
    if config.get('x_line') is not None:
        plt.axvline(x=config['x_line'], color='r', linestyle='--', label='Retirement')  # Vertical line
    plt.ylim(config.get('ylim', [0, 1000000]))
    plt.xlim(config.get('xlim', [0, 600]))
    plt.xlabel(config.get('xlabel', ''))
    plt.ylabel(config.get('ylabel', ''))
    plt.title(config.get('title', ''))
    plt.legend()


def generate_graphs(results_list):
    # Unpack the list of variables
    inflows, income_gains_storage, income_losses_storage, investment_gains_storage, assets_ending_list, assets_starting_list,  outflows, livret_A_list, livret_LDDS_list, livret_LEP_list, total_ending_list, ruined, variables = results_list

    retirement_age = int(variables['retirement_year']) * 12

    configs = [
        {'data': pd.Series(income_gains_storage).cumsum(), 'xlabel': 'Months', 'ylabel': 'Cumulative Income',
         'title': 'Cumulative Income Over Time', 'x_line': retirement_age, 'label': 'Income', 'ylim': [0, 400000]},

        {'data': pd.Series(investment_gains_storage).cumsum(), 'xlabel': 'Month',
         'ylabel': 'Cumulative Investment Returns', 'title': 'Cumulative Investment Returns Over Time', 'x_line': retirement_age, 'label': 'Investment'},

        {'data': pd.Series(income_losses_storage).cumsum(), 'xlabel': 'Month', 'ylabel': 'Common Outflows',
         'title': 'Cumulative Outflows Over Time', 'x_line': retirement_age, 'label': 'Outflows'},

        {'data': pd.Series(assets_ending_list), 'xlabel': 'Month', 'ylabel': 'Ending Asset Value',
         'title': 'Ending Asset Value after each period', 'x_line': retirement_age, 'label': 'Asset Value'},

         {'data': pd.Series(livret_A_list), 'xlabel': 'Month', 'ylabel': 'Savings Value',
         'title': 'Livret A after each period', 'x_line': retirement_age, 'label': 'Asset Value', 'ylim': [0, 100000]},

         {'data': pd.Series(livret_LDDS_list), 'xlabel': 'Month', 'ylabel': 'Savings Value',
         'title': 'Livret LDDS after each period', 'x_line': retirement_age, 'label': 'Asset Value', 'ylim': [0, 100000]},

         {'data': pd.Series(livret_LEP_list), 'xlabel': 'Month', 'ylabel': 'Savings Value',
         'title': 'Livret LEP after each period', 'x_line': retirement_age, 'label': 'Asset Value', 'ylim': [0, 50000]},

         {'data': pd.Series(total_ending_list), 'xlabel': 'Month', 'ylabel': 'Ending Total Value',
         'title': 'Ending Total Value after each period', 'x_line': retirement_age, 'label': 'Asset Value'},
    ]

    for i, config in enumerate(configs, start=1):
        plt.subplot(4, 2, i)
        plot_subplot(config['data'], config)

    plt.show()


# Define a function to generate a numeric summary report
def generate_metrics(results_list):
    # Unpack the list of variables
    inflows, income_gains_storage, income_losses_storage, income_after_saving, investment_gains_storage, assets_ending_list, assets_starting_list,  outflows, livret_A_list, livret_LDDS_list, livret_LEP_list, total_ending_list, ruined, variables = results_list

    # Create a DataFrame to store metrics
    months = int(variables['years'] * 12)
    metrics_df = pd.DataFrame(index=range(1, months))

    # Calculate and store metrics for each period
    metrics_df['Assets Starting'] = assets_starting_list[:-1]
    metrics_df['Outflow'] = [calculate_outflows(i, outflows, variables) for i in range(months - 1)]
    metrics_df['Assets Ending'] = assets_ending_list[:-1]
    
    # Adjust the length of investment_gains_storage and income_gains_storage to match other lists
    metrics_df['Investment Return'] = investment_gains_storage[:-1]
    metrics_df['Income'] = income_gains_storage[:-1]

    # Calculate additional metrics
    metrics_df['Net Cash Flow'] = metrics_df['Income'] - metrics_df['Outflow']
    metrics_df['Portfolio Value Change'] = metrics_df['Assets Ending'] - metrics_df['Assets Starting']
    metrics_df['Cumulative Returns'] = np.cumsum(metrics_df['Investment Return'])
    metrics_df['Drawdown'] = (metrics_df['Cumulative Returns'] - np.maximum.accumulate(metrics_df['Cumulative Returns'])) / np.maximum.accumulate(metrics_df['Cumulative Returns'])

    # save the results in a dataframe
    metrics_df.to_csv('./database/investment_summary.csv', index=False)

    # Display the DataFrame
    summary = metrics_df.describe(include='all')
    print(f"Summary for Assets starting, Outflow, etc.: \n\n  {summary}")


def transactions_summary(transactions_df):
    summary = pd.pivot_table(transactions_df, values='Amount', index='Type', aggfunc='sum')