def get_limits(capital=1_000_000):
    # limit = 20% of capital per asset
    return {
        "AAPL": capital * 0.2,
        "MSFT": capital * 0.2,
        "GOOG": capital * 0.2,
        "TSLA": capital * 0.2
    }