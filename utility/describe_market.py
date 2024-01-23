import pandas as pd
from matplotlib import pyplot as plt
from database.get_historic_data import get_market_history

def annual_market_returns(market_parameters):
    market_ticker,market_start_year,market_end_year = market_parameters

    # Download market history and convert it to a DataFrame
    market = get_market_history(market_parameters)
    market = pd.DataFrame(market, columns=['Adj Close'])

    # Generate group by keys
    market['date'] = market.index
    market['year'] = market['date'].apply(lambda d: f'{d.year}')

    # Group by year, take the adjusted close price of the first business day in each year
    df = market[['year', 'Adj Close']].sort_index().groupby('year').first()

    # Generate annual return
    df['return'] = df['Adj Close'].pct_change()

    # Show annual return by the beginning of next year
    df['return_next_y'] = df['return'].shift(-1)

    df = df.drop(columns='return')
    df = df.reset_index()

    # Plot the evolution through years
    print(df)

    x_values = range(len(df))  # Use len(df) for inclusive range
    plt.plot(df['return_next_y'], label=f'Market {market_ticker} evolution')
    plt.ylim([-1, 1])
    # Set x-axis ticks and labels using the DataFrame index
    plt.xticks(df.index, [str(year) for year in df.index + market_start_year], rotation=45, ha="right")

    plt.xlabel('Years')
    plt.ylabel('Return next year')
    plt.title('Evolution of the market throughout the years')
    plt.legend()

    # Describe the annual return
    print(f"\nAnnual return for {market_ticker} between {market_start_year} and {market_end_year}: \n {df['return_next_y'].describe()}")

    # Save the figure
    cleaned_market_name = market_ticker.translate(str.maketrans('', '', '^'))
    file_path = f'./outputs/{cleaned_market_name}_annual_return.png'
    plt.show()
    plt.savefig(file_path)  # Change the file extension based on your preferred format (e.g., '.png', '.jpg', '.pdf')
