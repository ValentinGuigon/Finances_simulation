from database.get_historic_data import get_monthly_average_return
import pandas as pd
import numpy as np

# Tweek the parameters to your liking
def get_starting_parameters(market_parameters):
        # Set up model
        inflows = {'active_annual_income':4800*12,
                'livret_A':11000,
                'livret_LDDS':10,
                'livret_LEP':0,
                'annual_rate_livret_A':0.03,
                'annual_rate_livret_LDDS':0.03,
                'annual_rate_livret_LEP':0.05,
                'max_livret_A':22950,
                'max_livret_LDDS':12000,
                'max_livret_LEP':10000,
                'starting_assets':0, # add value of starting assets
                'monthly_pension':3000, # add estimated post-retirement monthly pension
                'premium': 0} 

        strategy = {'saving_plan': inflows['max_livret_A'] + inflows['max_livret_LDDS'] + inflows['max_livret_LEP']
        }

        misc = {'food_beverages':1000,
                'sports':100,
                'arts':100,
                'nightlife':300,
                'phone_internet_and_so':100,
                'family':0}

        outflows = {'rent':1500,
                'credit_card_payment':30,
                'medical_insurance':350,
                'pension_contribution':0,
                'misc': np.mean(list(misc.values())),
                'retirement_medical_expenses':850, # add post-retirement monthly medical expenses
                'retirement_misc': 2000} # add post-retirement misc costs

        mkt_history_monthly_pct_return, mkt_history_monthly_std_dev = get_monthly_average_return(market_parameters)

        variables = {'start_date' : "03/01/2024",
                'date_of_birth': "10/19/1992",
                'state': "init",
                'years': 50, 
                'retirement_year': 36,
                'tax_on_active_income_gains': 0, # add our tax rate on active income in % terms
                'avg_ann_income_raise': 0.015, # add our annual salary raise in % terms
                'avg_ann_inflation': 0.015, # add annual inflation rate (mean inflation rate for France 1990-2020)
                'tax_on_investment_gains': 0.2, # add investment returns tax rate
                'avg_monthly_market_returns': mkt_history_monthly_pct_return, # add market return data to our inputs
                'avg_monthly_market_volatility': mkt_history_monthly_std_dev} # add market volatility data to our inputs

        parameters = {
        'inflows': inflows,
        'strategy': strategy,
        'misc': misc,
        'outflows': outflows,
        'variables': variables
        }

        return parameters


def get_new_parameters():
        # Define new states dictionaries
        update_us_salary = {'variables_start_date': '06/01/2024', 
        'variables_state': "updated",
        'inflows_active_annual_income': 6000*12}
        
        first_us_taxation = {'variables_start_date': '03/01/2026', 
        'variables_state': "updated",
        'variables_tax_on_active_income_gains': 0.2}

        back_to_france = {'variables_start_date': '03/01/2027', 
        'variables_state': "updated",
        'inflows_active_annual_income': 2800*12, 
        'variables_tax_on_active_income_gains': 0.25,
        'outflows_rent':800,
        'outflows_medical_insurance':60,
        'misc_food_beverages':400,
        'misc_sports':50}

        cr_classe_normale_at_cnrs = {'variables_start_date': '03/01/2030', 
        'variables_state': "updated",
        'inflows_active_annual_income': 2220*12, 
        'variables_tax_on_active_income_gains': 0.25, 
        'inflows_premium':3000,
        'outflows_rent':800,
        'outflows_medical_insurance':60,
        'misc_food_beverages':400,
        'misc_sports':50,
        'misc_family':500}

        cr_hors_classe_at_cnrs = {'variables_start_date': '03/01/2031', 
        'variables_state': "updated",
        'inflows_active_annual_income': 3010*12, 
        'variables_tax_on_active_income_gains': 0.25, 
        'inflows_premium':3000,
        'outflows_rent':800,
        'outflows_medical_insurance':60,
        'misc_food_beverages':400,
        'misc_sports':50,
        'misc_family':1000}

        dr_classe_2_at_cnrs = {'variables_start_date': '03/01/2033', 
        'variables_state': "updated",
        'inflows_active_annual_income': 3120*12, 
        'variables_tax_on_active_income_gains': 0.25, 
        'inflows_premium':3000,
        'outflows_rent':800,
        'outflows_medical_insurance':60,
        'misc_food_beverages':400,
        'misc_sports':50,
        'misc_family':1000}

        new_parameters_list = [
        update_us_salary,
        first_us_taxation, 
        back_to_france, 
        cr_classe_normale_at_cnrs, 
        cr_hors_classe_at_cnrs, 
        dr_classe_2_at_cnrs
        ]
        
        return new_parameters_list