import pandas as pd
import numpy as np
import random
from datetime import datetime as dt, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
from database.get_parameters import get_starting_parameters
from utility.calculation_functions import *

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
    inflows, income_gains_storage, income_losses_storage, income_after_saving, investment_gains_storage, assets_ending_list, assets_starting_list,  outflows, livret_A_list, livret_LDDS_list, livret_LEP_list, total_ending_list, ruined, variables, simulation_starting_date = results_list

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

    # Save the figure
    file_path = f'./outputs/annual_returns.png'
    plt.show()
    plt.savefig(file_path)  # Change the file extension based on your preferred format (e.g., '.png', '.jpg', '.pdf')


# Define a function to generate a numeric summary report
def generate_metrics(results_list):
    # Unpack the list of variables
    inflows, income_gains_storage, income_losses_storage, income_after_saving_storage, investment_gains_storage, assets_ending_list, assets_starting_list, outflows, livret_A_list, livret_LDDS_list, livret_LEP_list, total_ending_list, ruined, variables, simulation_starting_date = results_list

    # Create a DataFrame to store metrics
    months = int(variables['years'] * 12)
    metrics_df = pd.DataFrame(index=range(months))

    # Calculate and store metrics for each period part 1
    metrics_df['Period'] = range(1,months+1)
    type(simulation_starting_date)
    metrics_df['Date'] = [(dt.strptime(simulation_starting_date, '%m/%d/%Y') + timedelta(days=30 * period)).strftime('%m/%d/%Y') for period in range(months)]
    metrics_df['Income'] = income_gains_storage
    metrics_df['Outflows'] = income_losses_storage

    # Calculate and store metrics for each period part 2
    metrics_df['Begin Total Savings'] = [np.nan] + [sum(x) for x in zip(livret_A_list, livret_LDDS_list, livret_LEP_list)][:-1]
    metrics_df['Amount To Save'] = metrics_df['Income'] - metrics_df['Outflows']
    # metrics_df['Begin Livret A'] = [np.nan] + livret_A_list[:-1]
    # metrics_df['Begin Livret LDDS'] = [np.nan] + livret_LDDS_list[:-1]
    # metrics_df['Begin Livret LEP'] = [np.nan] + livret_LEP_list[:-1]
    # metrics_df['End Livret A'] = livret_A_list
    # metrics_df['End Livret LDDS'] = livret_LDDS_list
    # metrics_df['End Livret LEP'] = livret_LEP_list
    metrics_df['End Total Savings'] = [sum(x) for x in zip(livret_A_list, livret_LDDS_list, livret_LEP_list)]
    metrics_df['Savings Value Change'] = metrics_df['End Total Savings'] - metrics_df['Begin Total Savings']
    metrics_df['Savings Return'] = (metrics_df['End Total Savings'] - metrics_df['Begin Total Savings']) / metrics_df['Begin Total Savings']

    # Calculate and store metrics for each period part 3
    metrics_df['Begin Investment Portfolio'] = assets_starting_list
    metrics_df['Investment Return'] = investment_gains_storage
    metrics_df['Amount To Invest'] = income_after_saving_storage
    metrics_df['End Investment Portfolio'] = assets_ending_list
    metrics_df['Portfolio Value Change'] = metrics_df['End Investment Portfolio'] - metrics_df['Begin Investment Portfolio']
    metrics_df['Investment Return Rate'] = (metrics_df['End Investment Portfolio'] - metrics_df['Begin Investment Portfolio']) / metrics_df['Begin Investment Portfolio']
    metrics_df['Cumulative Returns'] = np.cumsum(metrics_df['Investment Return'])

    # Calculate and store metrics for each period part 4: Drawdown
    # Initialize the 'Drawdown' column with NaN
    metrics_df['Drawdown'] = np.nan  
    # Find the first non-zero and non-NaN index
    start_index = metrics_df['Cumulative Returns'].first_valid_index()
    # Calculate drawdown, but skip the initial rows with 0 or NaN
    for i in range(start_index, len(metrics_df)):
        cumulative_returns_slice = metrics_df['Cumulative Returns'].iloc[:i+1].dropna().values
        current_cumulative_return = metrics_df['Cumulative Returns'].iloc[i]
        max_cumulative_return = np.maximum.accumulate(cumulative_returns_slice[:-1])
        drawdown_value = 0 if len(max_cumulative_return) == 0 or np.isclose(max_cumulative_return[-1], 0) else (current_cumulative_return - max_cumulative_return[-1]) / max_cumulative_return[-1]
        metrics_df.loc[i, 'Drawdown'] = drawdown_value
    # Check for NaN or infinite values in the result
    if metrics_df['Drawdown'].isnull().any() or not np.isfinite(metrics_df['Drawdown']).all():
        print("There might be an issue with the data or calculation.")

    # Calculate and store metrics for each period part 5
    metrics_df['Begin Total Assets'] = [np.nan] + total_ending_list[:-1]
    metrics_df['End Total Assets'] = total_ending_list
    metrics_df['Total Assets Value Change'] = metrics_df['End Total Assets'] - metrics_df['Begin Total Assets']
    metrics_df['Total Assets Return Rate'] = (metrics_df['End Total Assets'] - metrics_df['Begin Total Assets']) / metrics_df['Begin Total Assets']
    
    metrics_df = metrics_df.round(2)

    # save the results in a dataframe
    metrics_df.to_csv('./outputs/investment_summary.csv', index=False)

    # Display the DataFrame
    summary = metrics_df.dropna(axis=0, how='any').describe(include='all')
    print(f"Summary for Assets starting, Outflow, etc.: \n\n  {summary}")


def transactions_summary(transactions_df):
    summary = pd.pivot_table(transactions_df, values='Amount', index='Type', aggfunc='sum')