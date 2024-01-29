from compute_gains import compute_gains
from gains.generate_reports import generate_graphs, generate_metrics
from gains.transaction_functions import add_income, add_expense
from gains.create_states import create_states
from gains.describe_market import annual_market_returns
from predict_retirement import predict_retirement

import pandas as pd
import numpy as np


# VARIABLES
market_ticker = "^SP500TR" # Choose the ticker for the market to simulate
market_start_year = 2009
market_end_year = 2023
market_parameters = [market_ticker, market_start_year, market_end_year]
generate_new_csv = True # True: generate states csv
include_update_states = True # True: simulate with new states as defined in get_historic_data.py


# Define new market parameters
if generate_new_csv == True:
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

# Simulate a retirement
predict_retirement()