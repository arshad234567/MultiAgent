import yfinance as yf
import pandas as pd
import os


def fetch_market_data(symbols):
    df = yf.download(symbols, period="3mo")

    # Handle multi-index safely
    if isinstance(df.columns, pd.MultiIndex):
        data = df["Close"]
    else:
        data = df[["Close"]].rename(columns={"Close": symbols[0]})

    data = data.dropna(how="all")

    returns = data.pct_change(fill_method=None)
    volatility = returns.rolling(10).std()

    return data, volatility


def save_raw_data(data):
    import os
    os.makedirs("data_store/raw", exist_ok=True)

    # Ensure proper column names
    data.columns = [str(col) for col in data.columns]

    for symbol in data.columns:
        df = data[[symbol]].dropna()

        print(f"Saving {symbol}...")  # debug

        df.to_csv(f"data_store/raw/{symbol}.csv", index=True)


def save_processed_data(data, volatility):
    os.makedirs("data_store/processed", exist_ok=True)

    data.to_csv("data_store/processed/prices.csv", index=True)
    volatility.to_csv("data_store/processed/volatility.csv", index=True)


if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "GOOG", "TSLA"]

    data, volatility = fetch_market_data(symbols)

    print("Downloaded data shape:", data.shape)

    save_raw_data(data)
    save_processed_data(data, volatility)

    print("Data fetched and saved successfully!")