from get_historic_data import download_SP500
import pandas as pd
import numpy as np

def get_personal_parameters():
        # Set up model
        inflows = {'active_annual_income':6000*12,
                'livret_A':11000,
                'livret_LDDS':10,
                'livret_LEP':0,
                'annual_rate_livret_A':0.03,
                'annual_rate_livret_LDDS':0.03,
                'annual_rate_livret_LEP':0.05,
                'max_livret_A':22950,
                'max_livret_LDDS':22950,
                'max_livret_LEP':10000,
                'starting_assets': 0, # add value of starting assets
                'monthly_pension': 2000, # add estimated post-retirement monthly pension
                'premium': 0} 

        strategy = {'saving_plan': inflows['max_livret_A'] + inflows['max_livret_LDDS'] + inflows['max_livret_LEP']
        }

        misc = {'food_beverages':1000,
                'sports':100,
                'arts':100,
                'nightlife':300,
                'phone_internet_and_so':100}

        outflows = {'rent':1500,
                'credit_card_payment':30,
                'medical_insurance':350,
                'pension_contribution':0,
                'misc': np.mean(list(misc.values())),
                'retirement_medical_expenses':850, # add post-retirement monthly medical expenses
                'retirement_misc': 2000} # add post-retirement misc costs

        sp_monthly_pct_return, sp_monthly_std_dev = download_SP500()

        variables = {'start_date' : "03/01/2024",
                'state': "init",
                'years': 36, 
                'retirement_year': 36,
                'tax_on_active_income_gains': 0, # add our tax rate on active income in % terms
                'avg_ann_income_raise': 0, # add our annual salary raise in % terms
                'avg_ann_inflation': 0.015, # add annual inflation rate (mean inflation rate for France 1990-2020)
                'tax_on_investment_gains': 0.2, # add investment returns tax rate
                'avg_monthly_market_returns': sp_monthly_pct_return, # add market return data to our inputs
                'avg_monthly_market_volatility': sp_monthly_std_dev} # add market volatility data to our inputs

        parameters = {
        'inflows': inflows,
        'strategy': strategy,
        'misc': misc,
        'outflows': outflows,
        'variables': variables
        }

        return parameters


def get_dummy_parameters():
        # Set up model
        inflows = {'active_annual_income':50_000,
                'livret_A':11000,
                'livret_LDDS':10,
                'livret_LEP':0,
                'annual_rate_livret_A':0.03,
                'annual_rate_livret_LDDS':0.03,
                'annual_rate_livret_LEP':0.05,
                'max_livret_A':22950,
                'max_livret_LDDS':22950,
                'max_livret_LEP':10000,
                'starting_assets': 250_000, # add value of starting assets
                'monthly_pension': 2000} # add estimated post-retirement monthly pension

        strategy = {'saving_plan': inflows['max_livret_A'] + inflows['max_livret_LDDS'] + inflows['max_livret_LEP']
        }

        misc = {'food_beverages':1000,
                'sports':100,
                'arts':100,
                'nightlife':300}

        outflows = {'rent':1500,
                'credit_card_payment':750,
                'medical_insurance':250,
                'pension_contribution':500,
                'misc': np.mean(list(misc.values())),
                'retirement_medical_expenses':850, # add post-retirement monthly medical expenses
                'retirement_misc': 2000} # add post-retirement misc costs

        sp_monthly_pct_return, sp_monthly_std_dev = download_SP500()

        variables = {'start_date' : "01/01/2020",
                'years': 40, 
                'retirement_year': 25, 
                'tax_on_active_income_gains': 0.25,
                'avg_ann_income_raise':0.05,
                'avg_ann_inflation': 0.02,
                'tax_on_investment_gains': 0.35,
                'avg_monthly_market_returns': sp_monthly_pct_return, 
                'avg_monthly_market_volatility': sp_monthly_std_dev}

        parameters = {
        'inflows': inflows,
        'strategy': strategy,
        'misc': misc,
        'outflows': outflows,
        'variables': variables
        }

        return parameters