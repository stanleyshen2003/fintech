import pandas as pd

def calculate_rsi(df, window=3):
    """Calculates the Relative Strength Index (RSI) for a given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        window (int, optional): The lookback window for RSI calculation. Defaults to 14.

    Returns:
        pd.Series: The calculated RSI series.
    """

    # Calculate price changes
    df['Price Change'] = df['Close'].diff()

    # Calculate gains and losses
    df['Gains'] = df['Price Change'].clip(lower=0)
    df['Losses'] = -df['Price Change'].clip(upper=0)

    # Calculate average gains and losses
    avg_gains = df['Gains'].rolling(window=window).mean()
    avg_losses = df['Losses'].rolling(window=window).mean()

    # Calculate RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Example usage
data = {'Close': [10, 12, 11, 13, 15, 14, 16, 18.5, 17, 19]}
df = pd.DataFrame(data)

rsi = calculate_rsi(df)
print(rsi)