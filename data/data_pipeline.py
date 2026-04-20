from data.generate_positions import generate_positions
from data.generate_limits import get_limits
from database.load_data import load_market_data
from services.breach_detector import detect_breach


def run():
    symbols = ["AAPL", "MSFT", "GOOG", "TSLA"]

    # Load data from DB
    data = load_market_data()
    data.set_index("Date", inplace=True)

    # 1.Get limits
    limits = get_limits()

    # Latest prices
    latest_prices = data.iloc[-1].to_dict()

    # Generate positions
    positions = generate_positions(
        symbols,
        latest_prices,
        limits,
        {}   # temporary
    )

    # Detect breaches
    breaches = detect_breach(positions, limits)

    print("\n Positions:")
    for p in positions:
        print(p)

    print("\n Breaches:")
    print(breaches)


if __name__ == "__main__":
    run()