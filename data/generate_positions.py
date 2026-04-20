import random

def allocate_portfolio(symbols):
    weights = [random.uniform(0.1, 0.4) for _ in symbols]
    total = sum(weights)
    weights = [w / total for w in weights]
    return dict(zip(symbols, weights))


def generate_positions(symbols, latest_prices, limits, volatility):
    positions = []

    capital = 1_000_000
    # total desk capital

    weights = allocate_portfolio(symbols)

    for symbol in symbols:
        price = latest_prices[symbol]
        weight = weights[symbol]

        allocated_money = capital * weight
        quantity = int(allocated_money / price)

        # 🔥 volatility impact (realistic behavior)
        if volatility[symbol] > 0.03:
            quantity = int(quantity * 1.2)

        value = quantity * price

        positions.append({
            "trader_id": f"T{random.randint(100, 999)}",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "value": value,
            "weight": round(weight, 2)
        })

    return positions