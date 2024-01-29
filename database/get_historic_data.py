import pandas as pd
import datetime
import yfinance as yf
import numpy as np

def download_market_history(market_ticker, market_start_year, market_end_year):
    # download S&P historic prices data
    start, end = datetime.datetime(market_start_year, 12, 31), datetime.datetime(market_end_year, 1, 1)
    ticker = market_ticker
   
    # To download the S&P historic prices data, you can use the ticker of "^SP500TR"
    # If you want to use the price index of SP500, you can use the ticker of "^GSPC"
    # SP = pdr.get_data_yahoo("^GSPC", start=startdate, end=enddate)

    # Fetch data from Yahoo Finance
    market_history = yf.download(ticker, start=start, end=end)['Adj Close']

    return market_history


def get_monthly_average_return(market_parameters):
    market_ticker, market_start_year, market_end_year = market_parameters
    
    market_history = download_market_history(market_ticker, market_start_year, market_end_year)

    # Calculate average monthly return & volatility
    mkt_history_monthly_pct_return = market_history.resample('M').last().pct_change().mean()
    mkt_history_monthly_std_dev = market_history.resample('M').last().pct_change().std()
    print(f"Monthly average return: mean={np.round(mkt_history_monthly_pct_return, decimals=4)}, sd={np.round(mkt_history_monthly_std_dev, decimals=4)}")

    return mkt_history_monthly_pct_return, mkt_history_monthly_std_dev


def get_market_history(market_parameters):
    market_ticker, market_start_year, market_end_year = market_parameters
    
    market_history = download_market_history(market_ticker, market_start_year, market_end_year)

    return market_history