import numpy as np
import pandas as pd

def generate_correlation_matrix():
    # These estimate came out of an older report (2019-2020) from BNY Mellon: 
    # https://www.bnymellonwealth.com/content/dam/bnymellonwealth/pdf-library/articles/202310YearCapitalMarketAssumptions.pdf
    corr_matrix = np.array([[1.00,  0.23, -0.15, -0.12, -0.05],
                            [0.23,  1.00, -0.33, -0.19, -0.19],
                            [-0.15, -0.33,  1.00,  0.39,  0.75],
                            [-0.12, -0.19,  0.39,  1.00,  0.55],
                            [-0.05, -0.19,  0.75,  0.55,  1.00]])

    return corr_matrix

def generate_expected_return_and_volatility():
    # Define expected returns and volatility
    exp_ret = np.array([2.1, 2.3, 6.1, 2.0, 8.3]) / 100
    vol = np.array([0.6, 4.2, 15.0, 15.4, 22.9]) / 100

    return exp_ret, vol

def generate_covariance_matrix(corr_matrix, vol):
    # Generate covariance matrix from correlation matrix and volatility
    cov_matrix = np.zeros((5, 5))
    for i, row in enumerate(corr_matrix):
        for j, col in enumerate(row):
            cov_matrix[i, j] = col * vol[i] * vol[j]

    return cov_matrix

def load_stock_returns(file_path='./retirement/SP500_data.csv'):
    # Load S&P 500 returns data
    stock_ret = pd.read_csv(file_path)
    modern_ret = stock_ret.loc[948:].copy()

    return modern_ret

# Additional functions for data manipulation or loading can be added here if needed.
