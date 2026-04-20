import yfinance as yf
import pandas as pd

def fetch_market_data(symbols):
    data = yf.download(symbols, period="3mo")["Close"]

    returns = data.pct_change(fill_method=None)
    volatility = returns.rolling(10).std()

    return data, volatility