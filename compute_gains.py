import os
import pandas as pd
import numpy as np
import random
import datetime
from gains.calculation_functions import *
from gains.update_functions import *

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


# Define a function to generate graphic summary reports
def compute_gains(init_states_df, updated_states_df):
    economic_states_df = init_states_df

    # Unpack the parameters for the next iteration
    inflows, outflows, strategy, misc, variables = unpack_parameters_from_dataframe(economic_states_df, 'inflows', 'outflows', 'strategy', 'misc', 'variables')

    # create lists to store each period's income, investments, savings and assets
    income_gains_storage = []
    income_losses_storage = []
    income_after_saving_storage = []
    investment_gains_storage = [] 
    assets_ending_list = []
    livret_A_list, livret_LDDS_list, livret_LEP_list = [], [], []

    assets_starting_list = [inflows['starting_assets']]
    savings_plan_storage = [sum([inflows['livret_A'], inflows['livret_LDDS'], inflows['livret_LEP']])]

    months = int(variables['years'] * 12)
    simulation_starting_date = variables['start_date']
    ruined = False # signals if we have become financially "ruined"
    
    for month in range(months):
        
        # store the parameters in a dictionnary
        parameters = {
            'inflows': inflows,
            'strategy': strategy,
            'misc': misc,
            'outflows': outflows,
            'variables': variables
            }

        # check if first time through the loop
        # if yes, initiate the assets_starting_list and the savings_plan_storage
        # if not, previous period ending assets are this period's starting assets
        if assets_ending_list:
            assets_starting_list.append(assets_ending_list[-1])

            #  and check for potential updates in the states
            if updated_states_df.loc[month - 1, 'variables_state'] == "updated":
                filtered_df = updated_states_df.loc[month - 1:month - 1,:] # only some columns are completed
                filtered_df = filtered_df.fillna(economic_states_df.iloc[-1, :]) # for the empty columns we take parameters from the state of the previous period
                inflows, strategy, misc, outflows, variables = update_parameters_from_dataframe(filtered_df, parameters)
                
            else: # else use the last state
                filtered_df = economic_states_df.iloc[-1, :]
                inflows, strategy, misc, outflows, variables = update_parameters_from_dataframe(economic_states_df, parameters)
        
        
        # create a variable to keep track of our assets value
        assets = assets_starting_list[-1]


        # we calculate income gains (including retirement and taxes)
        income = calculate_income(month, inflows, variables)
        income_gains_storage.append(income)


        # then we subtract our monthly costs from our income and take into account the inflation
        outflow = calculate_outflows(month, outflows, variables)
        income -= outflow
        income_losses_storage.append(outflow)

        # check if asset base has a pos. value; if not then set the "ruined" flag to 1 and end the simulation
        if assets < 0:
            ruined = True
            break

        # generate a monthly market return for our "assets" variable by drawing from a normal distribution
        # apply the tax rate to investment gains then add investment returns to our "assets" variable
        investment_return = calculate_investment_gains(assets, variables)
        investment_gains_storage.append(investment_return)
        assets += investment_return 


        # check if savings has a pos. value; if not then set the "ruined" flag to 1 and end the simulation
        if sum(savings_plan_storage) < 0:
            ruined = True
            break
        
        # generate a monthly savings return with updating savings in each account
        # also, update saving plan storage and store the evolution of each livret
        inflows['livret_A'], inflows['livret_LDDS'], inflows['livret_LEP'] = calculate_savings_gains(inflows)
        savings_plan_storage.append(inflows['livret_A'] + inflows['livret_LDDS'] + inflows['livret_LEP'])
        livret_A_list.append(inflows['livret_A'])
        livret_LDDS_list.append(inflows['livret_LDDS'])
        livret_LEP_list.append(inflows['livret_LEP'])


        # then follow the savings strategy to update savings and put the rest in the assets
        inflows, income_after_saving, savings_plan_storage = update_savings(inflows, income, strategy, savings_plan_storage)
        assets += income_after_saving
        income_after_saving_storage.append(income_after_saving)


        # calculate the end of period
        assets_ending = assets 
        assets_ending_list.append(assets_ending) # store ending assets value
        total_ending_list = [sum(x) for x in zip(assets_ending_list, livret_A_list, livret_LDDS_list, livret_LEP_list)]


        # update the date
        new_start_date_string = (pd.to_datetime(variables['start_date'], format='%m/%d/%Y') + pd.DateOffset(months=1)).strftime('%m/%d/%Y')
        variables['start_date'] = new_start_date_string


        # update the parameters
        parameters = {
        'inflows': inflows,
        'strategy': strategy,
        'misc': misc,
        'outflows': outflows,
        'variables': variables
        }


        # Update the state dataframe with the parameters from this period
        economic_states_df = update_state_df(economic_states_df, parameters_to_dataframe(parameters))


    # save the resulting economic projection
    economic_states_df.to_csv('./database/economic_projections.csv', index=False)


    return [inflows, income_gains_storage, income_losses_storage, income_after_saving_storage, investment_gains_storage, assets_ending_list, assets_starting_list, outflows, livret_A_list, livret_LDDS_list, livret_LEP_list, total_ending_list, ruined, variables, simulation_starting_date]

