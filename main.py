from compute_gains import compute_gains
from reports import generate_graphs, generate_metrics
from utility.transaction_functions import add_income, add_expense
from utility.create_states import run_states
from utility.describe_market import annual_market_returns

import pandas as pd
import numpy as np


# VARIABLES
market_ticker = "^SP500TR" # Choose the ticker for the market to simulate
market_start_year = 2009
market_end_year = 2023
market_parameters = [market_ticker,market_start_year,market_end_year]
define_new_states = False # True: generate init_states & update_states csv


# Get the parameters for the model into a Dataframe
if define_new_states == True:
    run_states(update=True, market_parameters=market_parameters)
init_states_df = pd.read_csv ('./database/init_states.csv')
updated_states_df = pd.read_csv ('./database/updated_states.csv')


# Create a Pandas DataFrame to store the financial transactions
TRANSACTION_COLUMNS = ['Date', 'Type', 'Amount']
transactions_df = pd.DataFrame(columns=TRANSACTION_COLUMNS)


# Describe the annual return of a specific market 
annual_market_returns = annual_market_returns(market_parameters)

# When checking the annual return rate, the minimum value is -0.05% and maximum value is 38.7%. In case it were from -34.1 to 38.7, for instance, we should not be panic if we see a drop of 30-40% in the total value in a certain year. In such cases, try to buy more in the dip, and the bull market will follow in 1-3 years.


# Compute gains
results_list = compute_gains(init_states_df, updated_states_df)


# Generate graphs and metrics
generate_graphs(results_list)
generate_metrics(results_list)


# # Plan new states here, such as economic shocks (e.g., change of income, early retirement, expensive rent, etc.):
# new_state = apply_shocking_state(economic_states_df, starting_period = 37, ending_period = variables['years']*12, 
#      credit_card_payment = 650, pension_contribution = 250)
# # specify the starting and ending period as well as the parameters you wish to change

