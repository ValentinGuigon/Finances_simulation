import pandas as pd
import numpy as np
import random
# change syntax and name of Pandas DataReader import
from pandas_datareader import data as pdr
# import yfinance as pandas data-reader currently not stable
import yfinance as yf
import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt


def calculate_outflows(month, outflows, variables):
    
    # logic to account for different outflows in retirement
    if month >= variables['retirement_year'] * 12:
        outflow = outflows['retirement_medical_expenses'] + outflows['retirement_misc']
    
    else:
        # logic to account for different outflows before retirement
        outflow = (outflows['rent'] + outflows['credit_card_payment'] + \
              outflows['medical_insurance'] + outflows['pension_contribution'] + \
              outflows['misc'])
    
    # each year, increment the values according to the annual inflation input 
    if (month % 12 == 0) and (month > 0):
        outflows['rent'] *= (1 + (variables['avg_ann_inflation']))
        outflows['credit_card_payment'] *= (1 + (variables['avg_ann_inflation']))
        outflows['medical_insurance'] *= (1 + (variables['avg_ann_inflation']))
        outflows['pension_contribution'] *= (1 + (variables['avg_ann_inflation']))
        outflows['misc'] *= (1 + (variables['avg_ann_inflation']))
        
    return outflow

    
def calculate_income(month, inflows, variables):
    
    # logic to account for different inflows in retirement
    if month >= variables['retirement_year'] * 12:
        income = inflows['monthly_pension']
    
    else: 
        # logic to account for different inflows before retirement
        income = (inflows['active_annual_income'] * (1 - variables['tax_on_active_income_gains'])) / 12
        if (month % 12 == 0) and (month > 0):
            inflows['active_annual_income'] *= (1 + (variables['avg_ann_income_raise']))
            
    return income


def calculate_investment_gains(assets, variables):
    if assets <= 0:
        inv_gains = 0
    
    else:
        market_return = np.random.normal(variables['avg_monthly_market_returns'], 
                                         variables['avg_monthly_market_volatility'],
                                        1)[0]
        inv_gains = (assets * market_return) * (1 - variables['tax_on_investment_gains'])
    return inv_gains
    

# set the numpy random seed to allow replication of results
np.random.seed(seed=7)
start, end = datetime.datetime(2000, 12, 31), datetime.datetime(2020, 1,1)

# add yfinance-pandas data-reader overide (now we can use pandas data-reader methods again as currently unstable)
yf.pdr_override()
# change our download to use new over-ridden method
sp = pdr.get_data_yahoo("^SP500TR", start=start, end=end)

sp_monthly_pct_return = sp.resample('M').last().pct_change().mean().values[0]
sp_monthly_std_dev = sp.resample('M').last().pct_change().std().values[0]

inflows = {'active_annual_income':50_000,
           'starting_assets': 250_000,
           'monthly_pension': 1500} 

outflows = {'rent':1500,
            'credit_card_payment':750,
            'medical_insurance':250,
            'pension_contribution':500,
            'misc': 1500,
            'retirement_medical_expenses':850, 
            'retirement_misc': 2000} 

variables = {'start_date' : "01/01/2020",
             'years': 40, 
             'retirement_year': 25, 
             'tax_on_active_income_gains': 0.25,
             'avg_ann_income_raise':0.05,
             'avg_ann_inflation': 0.02,
             'tax_on_investment_gains': 0.35,
             'avg_monthly_market_returns': sp_monthly_pct_return, 
             'avg_monthly_market_volatility': sp_monthly_std_dev} 
income_gains_storage = []
investment_gains_storage = [] 

assets_starting_list = [inflows['starting_assets']] 
assets_ending_list = [] 
months = variables['years'] * 12

ruined = False

for month in range(months):
    if assets_ending_list:
        assets_starting_list.append(assets_ending_list[-1])
        
    assets = assets_starting_list[-1]
    
    outflow = calculate_outflows(month, outflows, variables)
    
    assets -= outflow
    
    # altered the ``if`` code block below to account for use of new function
    if assets <= 0:
        ruined = True
        break
    
    # use our new function to calculate investment returns
    investment_return = calculate_investment_gains(assets, variables)
  
    investment_gains_storage.append(investment_return)
    assets += investment_return
    
    income = calculate_income(month, inflows, variables)
    income_gains_storage.append(income)
    
    assets += income
    assets_ending = assets
    assets_ending_list.append(assets_ending)  
    
   
plt.plot(pd.Series(assets_ending_list))
plt.xlabel('Month')
plt.ylabel('Ending Asset Value')
plt.show()
