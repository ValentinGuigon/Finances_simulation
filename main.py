from compute_gains import compute_gains
from reports import generate_graphs, generate_metrics
from utility.transaction_functions import add_income, add_expense
from utility.create_states import create_states
from utility.describe_market import annual_market_returns

import pandas as pd
import numpy as np


# VARIABLES
market_ticker = "^SP500TR" # Choose the ticker for the market to simulate
market_start_year = 2009
market_end_year = 2023
generate_new_csv = True # True: generate states csv
include_update_states = True # True: simulate with new states as defined in get_historic_data.py

# Define new market parameters
if generate_new_csv == True:
    market_parameters = [market_ticker, market_start_year, market_end_year]
    create_states(update=include_update_states, market_parameters=market_parameters)

# Get the parameters for the model into a Dataframe
init_states_df = pd.read_csv ('./database/init_states.csv')
updated_states_df = pd.read_csv ('./database/updated_states.csv')

# Create a Pandas DataFrame to store the financial transactions
TRANSACTION_COLUMNS = ['Date', 'Type', 'Amount']
transactions_df = pd.DataFrame(columns=TRANSACTION_COLUMNS)


# Describe the annual return of a specific market 
annual_market_returns = annual_market_returns(market_parameters)


# Compute gains
results_list = compute_gains(init_states_df, updated_states_df)


# Generate graphs and metrics
generate_graphs(results_list)
generate_metrics(results_list)


# # Plan new states here, such as economic shocks (e.g., change of income, early retirement, expensive rent, etc.):
# new_state = apply_shocking_state(economic_states_df, starting_period = 37, ending_period = variables['years']*12, 
#      credit_card_payment = 650, pension_contribution = 250)
# # specify the starting and ending period as well as the parameters you wish to change

