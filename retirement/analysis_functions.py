import numpy as np
import pandas as pd
import statsmodels.api as sm
from numpy import matlib
from scipy.optimize import minimize
from scipy.stats import norm
import warnings


def analyze_spx_returns(exp_ret, vol):
    # Analyze S&P 500 returns
    mu = (1 + exp_ret[2]) ** (1 / 12) - 1
    sigma = vol[2] / (12 ** 0.5)
    stock_ret = pd.read_csv('./retirement/SP500_data.csv')
    modern_ret = stock_ret.loc[948:].copy()
    mth_ret = modern_ret['SP500'] / modern_ret['SP500'].shift(1) - 1

    return mu, sigma, mth_ret


def calculate_theoretical_actual_probability(mu, sigma, mth_ret):
    # Look at how the frequency of extreme events compare between normal distribution and S&P 500
    target = (mu - 2.7 * sigma)
    theoretical_probability = norm.cdf(x=target, loc=mu, scale=sigma) * 100
    actual_probability = mth_ret[mth_ret <= target].shape[0] / mth_ret[1:].shape[0] * 100

    return theoretical_probability, actual_probability


def calculate_z_scores(mth_ret, mu, sigma):
    # Calculate Z scores of the worst monthly S&P 500 returns
    target = (mu - 2.7 * sigma)
    worst_ret = sorted(mth_ret[mth_ret <= target])
    z_score = [(i - mu) / sigma for i in worst_ret]

    return z_score


def ret_var(W, cov_matrix, exp_ret):
    return -np.dot(exp_ret, W) + (W @ cov_matrix @ W.T)


def optimize_portfolio(W0, cov_matrix, exp_ret, vol, verbose):
    # Find the optimal portfolio using mean-variance optimization and return the optimal weights, W
    args = (cov_matrix, exp_ret)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},                 # weights must sum to 1
                   {'type': 'eq', 'fun': lambda x: (x @ cov_matrix @ x.T) ** 0.5 - vol})  # vol must = 0.10
    bounds = tuple((0, 1) for asset in range(W0.shape[0]))                          # no shorts

    # Run the optimizer 
    optimal = minimize(ret_var, W0, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    W = optimal.x

    W_dict = {'T_Bills': W[0],
              'T_Bonds': W[1],
              'LC_Stocks': W[2],
              'Commodities': W[3],
              'EM_Stocks': W[4]}
    if verbose:
        # print(W_dict, '\n')
        # print(np.sum(W), '\n')
        print('Expected Return: %.3f' % np.dot(W, exp_ret))
        print('Expected Volatility: %.3f' % (W @ cov_matrix @ W.T) ** 0.5)
        print('Percent Invested in Stocks: %.3f' % np.sum(W[2:]))
    return W_dict, W


def get_wealths(parameters, W, L, corr_returns, real=False, spend=28, infl=0.02):
    pre_ret, N, start_wealth, sims = parameters
    
    # If real is True, calculate inflation adjusted returns
    # For each year, matrix multiply the individual asset returns by W, portfolio weights to get portfolio return
    # returns is a 
    returns = np.ones((N, len(corr_returns)))
    for i, ret in enumerate(corr_returns):
        if real:
            returns[:,i] = 1 + ret@np.array(W).T - np.random.normal(infl, 0.01, (N))   # returns
        else:
            returns[:,i] = 1 + ret@np.array(W).T
    returns = pd.DataFrame(returns)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=pd.errors.PerformanceWarning)

        # Get the wealths by year, basically for each year we subtract out the spending and then apply the portfolio return
        wealth_df = pd.DataFrame()
        for sim in range(sims):
            wealth = [start_wealth]
            for yr in range(N):
                if yr >= pre_ret:
                    wealth.append((wealth[yr] - spend)*returns.loc[yr, sim])
                else:
                    wealth.append((wealth[yr] - 0)*returns.loc[yr, sim])
            wealth_df[sim] = wealth
            
        perc_df = pd.DataFrame()
        perc_df[5] = wealth_df.quantile(0.05, axis=1)
        perc_df[50] = wealth_df.quantile(0.50, axis=1)
        perc_df[95] = wealth_df.quantile(0.95, axis=1)
        return perc_df, wealth_df


def simulate_portfolio(W0, corr_matrix, cov_matrix, exp_ret, vol, sims, N):
    """
    Simulate portfolio returns.

    Parameters:
    - W0: Initial portfolio weights
    - cov_matrix: Covariance matrix of asset returns
    - exp_ret: Expected returns of assets
    - vol: Volatility of assets
    - sims: Number of simulations
    - N: Number of years

    Returns:
    - corr_returns: Simulated correlated portfolio returns
    """
    
    # Portfolio Simulation
    L = np.linalg.cholesky(corr_matrix)
    corr_returns = []
    for i in range(sims):
        corr_shocks = np.random.normal(0, 1, (N, exp_ret.shape[0])) @ L.T
        corr_returns.append(np.matlib.repmat(exp_ret, N, 1) + np.matlib.repmat(vol, N, 1) * corr_shocks)

    # Optimize Portfolio
    W_dict, W = optimize_portfolio(W0, cov_matrix, exp_ret, vol=0.10, verbose=True)

    return W_dict, W, L, corr_returns


def calculate_failure_rate(wealths, sims):
    # Calculate the failure rate (frequency of running out of money)
    failure_rate = len([i for i in wealths.loc[30] if i < 0]) / sims

    return failure_rate
