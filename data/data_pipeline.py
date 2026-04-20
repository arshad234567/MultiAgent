from data.fetch_market_data import fetch_market_data
from data.generate_positions import generate_positions
from data.generate_limits import get_limits
from services.breach_detector import detect_breach


def run():
    symbols = ["AAPL", "MSFT", "GOOG", "TSLA"]

    # Fetch real market data
    data, volatility = fetch_market_data(symbols)

    # Get limits
    limits = get_limits()

    # Latest prices
    latest_prices = data.iloc[-1].to_dict()

    # Latest volatility
    latest_volatility = volatility.iloc[-1].to_dict()

    # Generate realistic positions
    positions = generate_positions(
        symbols,
        latest_prices,
        limits,
        latest_volatility
    )

    # Detect breaches
    breaches = detect_breach(positions, limits)

    print("\n📊 Positions:")
    for p in positions:
        print(p)

    print("\n🚨 Breaches:")
    print(breaches)


if __name__ == "__main__":
    run()