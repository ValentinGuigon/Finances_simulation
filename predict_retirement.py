import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import norm
from retirement.data_setup import generate_correlation_matrix, generate_expected_return_and_volatility, generate_covariance_matrix, load_stock_returns
from retirement.plots_functions import plot_correlation_matrix, plot_qq_plot, plot_wealth_simulation, plot_wealth_histogram
from retirement.analysis_functions import analyze_spx_returns, calculate_theoretical_actual_probability, calculate_z_scores, simulate_portfolio, get_wealths, calculate_failure_rate


def predict_retirement():
    # Set random seed for reproducibility
    np.random.seed(42)

    # Get the parameters from the gains simulation
    economic_projections = pd.read_csv("./database/economic_projections.csv")
    investment_summary = pd.read_csv("./outputs/investment_summary.csv")

    start_date = datetime.strptime(economic_projections['variables_start_date'].iloc[0], "%m/%d/%Y")
    birth_date = datetime.strptime(economic_projections['variables_date_of_birth'].iloc[0], "%m/%d/%Y")

    # Constants
    start_age = int((economic_projections['variables_retirement_year'].iloc[0] + (start_date - birth_date).days // 365))
    pre_ret = 0                                                                     # 0 more years to go before retirement
    post_ret = 30                                                                   # years before death
    N = post_ret                                                                    # total number of years
    start_wealth = investment_summary['End Total Assets'].iloc[-1]/1000             # in $USD Thousands
    spend = (economic_projections['inflows_monthly_pension'].iloc[0]*12)/1000       # in $USD Thousands
    sims = 5000

    W0 = np.array([0.1, 0.2, 0.5, 0.1, 0.2])
    parameters = [pre_ret, N, start_wealth, sims]
    spend2 = spend+10


    # Load and set up data
    corr_matrix = generate_correlation_matrix()
    exp_ret, vol = generate_expected_return_and_volatility()
    cov_matrix = generate_covariance_matrix(corr_matrix, vol)
    stock_ret = load_stock_returns()

    # Analyze S&P 500 returns, Z scores and Extreme Events
    mu, sigma, mth_ret = analyze_spx_returns(exp_ret, vol)
    z_scores = calculate_z_scores(mth_ret, mu, sigma)
    theoretical_prob, actual_prob = calculate_theoretical_actual_probability(mu, sigma, mth_ret)


    # Plot correlation matrix:
    plot_correlation_matrix(corr_matrix)

    # Plot QQ plot and Extreme Event Analysis:
    plot_qq_plot(mth_ret, mu, sigma)
    print(f'Theoretical probability of extreme events in a normal distribution = {theoretical_prob:.2f} %')
    print(f'Actual probability of extreme events in S&P500 from 1871 to 2018 = {actual_prob:.2f} %')


    # Generate portfolio returns from correlated, random variables
    W_dict, W, L, corr_returns = simulate_portfolio(W0, corr_matrix, cov_matrix, exp_ret, vol, sims, N)

    # Forecasts the wealths based on simulated asset class returns, inflation, and spending
    perc_df_scenario1, wealths_scenario1 = get_wealths(parameters, W, L, corr_returns, real=True, spend=spend)

    perc_df_scenario2, wealths_scenario2 = get_wealths(parameters, W,  L, corr_returns, real=True, spend=spend2)


    # Plot Wealth Simulation and comparisons
    plot_wealth_simulation(perc_df_scenario1, perc_df_scenario2, N, start_age)
    plot_wealth_histogram(wealths_scenario1, spend, wealths_scenario2, spend2)


    # Calculate Failure Rate
    print(f'Failure Rate for scenario 1: {calculate_failure_rate(wealths_scenario1, sims):.2%}')
    print(f'Failure Rate for scenario 1: {calculate_failure_rate(wealths_scenario2, sims):.2%}')


if __name__ == "__main__":
    # Call the function with some placeholder results_list
    predict_retirement()