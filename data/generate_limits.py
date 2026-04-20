def get_limits(capital=1_000_000):
    return {
        "AAPL": capital * 0.25,
        "MSFT": capital * 0.2,
        "GOOG": capital * 0.3,
        "TSLA": capital * 0.15
    }