from fetch_market_data import fetch_market_data
from generate_positions import generate_positions
from generate_limits import get_limits
from services.breach_detector import detect_breach


def run():
    symbols = ["AAPL", "MSFT", "GOOG", "TSLA"]

    data, volatility = fetch_market_data(symbols)

    positions = generate_positions(symbols)

    limits = get_limits()

    latest_prices = data.iloc[-1].to_dict()

    breaches = detect_breach(positions, latest_prices, limits)

    print("Breaches:", breaches)


if __name__ == "__main__":
    run()