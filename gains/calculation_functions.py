import pandas as pd
import numpy as np
import random
import datetime

def calculate_income(month, inflows, variables):
    
    # add logic to account for pension received in retirement with no salary
    # if retired
    if month >= variables['retirement_year'] * 12:
        income = inflows['monthly_pension']
    
    else: 
        if (month % 12 == 0) and (month > 0): # we dont want to apply the raise on the very first month
            # every 12 months we increase our base salary by the average annual percentage increase
            inflows['active_annual_income'] *= (1 + (variables['avg_ann_income_raise']))

        # add the effect of the tax rate being applied to our income
        income = (inflows['active_annual_income'] * (1 - variables['tax_on_active_income_gains'])) / 12

        # if this is the end of the year, we gain a premium minus the tax
        if pd.to_datetime(variables['start_date'], format='%m/%d/%Y').month == 12:
            income += (inflows['premium'] * (1 - variables['tax_on_active_income_gains']))
            
    return income


def calculate_outflows(month, outflows, variables):
    # add logic to account for different outflows in retirement
    # if retired
    if month >= variables['retirement_year'] * 12:
        outflow = outflows['retirement_medical_expenses'] + outflows['retirement_misc']
    
    else:
        outflow = (outflows['rent'] + outflows['credit_card_payment'] + \
              outflows['medical_insurance'] + outflows['pension_contribution'] + \
              outflows['misc'])
    
    # each year, increment the values according to the annual inflation input (individual listing to enable customisation)
    if (month % 12 == 0) and (month > 0):
        outflows['rent'] *= (1 + (variables['avg_ann_inflation']))
        outflows['credit_card_payment'] *= (1 + (variables['avg_ann_inflation']))
        outflows['medical_insurance'] *= (1 + (variables['avg_ann_inflation']))
        outflows['pension_contribution'] *= (1 + (variables['avg_ann_inflation']))
        outflows['misc'] *= (1 + (variables['avg_ann_inflation']))
        
    return outflow


def calculate_investment_gains(assets, variables):
    if assets <= 0:
        inv_gains = 0
    
    else:
        market_return = np.random.normal(variables['avg_monthly_market_returns'], 
                                         variables['avg_monthly_market_volatility'],
                                        1)[0]
        inv_gains = (assets * market_return) * (1 - variables['tax_on_investment_gains'])
    return inv_gains


def calculate_savings_gains(inflows):
    # Calculate monthly rates
    monthly_rate_livret_A = inflows['annual_rate_livret_A'] / 12
    monthly_rate_livret_LDDS = inflows['annual_rate_livret_LDDS'] / 12
    monthly_rate_livret_LEP = inflows['annual_rate_livret_LEP'] / 12
    
    # Calculate monthly gains for each account
    # The rate only applies to the amount up to the livret maximum limit
    inflows['livret_A'] += min(inflows['max_livret_A'], inflows['livret_A']) * monthly_rate_livret_A

    inflows['livret_LDDS'] += min(inflows['max_livret_LDDS'], inflows['livret_LDDS']) * monthly_rate_livret_LDDS

    inflows['livret_LEP'] += min(inflows['max_livret_LEP'], inflows['livret_LEP']) * monthly_rate_livret_LEP
    
    return inflows['livret_A'], inflows['livret_LDDS'], inflows['livret_LEP']


def allocate_income_to_account(inflows, income, livret_key, max_livret_key, strategy, savings_plan_storage):
    # Check if the livret has not reached the maximum
    if savings_plan_storage[-1] != strategy['saving_plan']:
        if inflows[livret_key] < inflows[max_livret_key]:
            # Calculate the available space in the livret
            available_space = inflows[max_livret_key] - inflows[livret_key]
            # Allocate the income to the livret, considering available space
            allocated_amount = min(available_space, income)
            inflows[livret_key] += allocated_amount
            income -= allocated_amount

    return inflows, income, savings_plan_storage


def update_savings(inflows, income, strategy, savings_plan_storage):
    
    # Allocate income to livrets
    inflows, income, savings_plan_storage = allocate_income_to_account(inflows, income, 'livret_LEP', 'max_livret_LEP', strategy, savings_plan_storage)
    inflows, income, savings_plan_storage = allocate_income_to_account(inflows, income, 'livret_A', 'max_livret_A', strategy, savings_plan_storage)
    inflows, income, savings_plan_storage = allocate_income_to_account(inflows, income, 'livret_LDDS', 'max_livret_LDDS', strategy, savings_plan_storage)

    income_after_saving = income

    return inflows, income_after_saving, savings_plan_storage