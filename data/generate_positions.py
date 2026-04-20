import random

import random


def allocate_portfolio(symbols):
    n = len(symbols)

    # Start with equal distribution
    base_weight = 1 / n

    weights = []

    for _ in symbols:
        # small variation around equal weight
        variation = random.uniform(-0.05, 0.05)
        w = base_weight + variation
        weights.append(max(0.05, w))  # ensure minimum

    # Normalize
    total = sum(weights)
    weights = [w / total for w in weights]

    return dict(zip(symbols, weights))


def generate_positions(symbols, latest_prices, limits, volatility):
    positions = []

    capital = 1_000_000  # total desk capital
    weights = allocate_portfolio(symbols)

    for symbol in symbols:
        price = latest_prices[symbol]
        weight = weights[symbol]

        allocated_money = capital * weight
        quantity = int(allocated_money / price)


        vol = volatility.get(symbol, 0)

        if vol > 0.03:
            quantity = int(quantity * 1.2)

        value = quantity * price

        positions.append({
            "trader_id": f"T{random.randint(100, 999)}",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "value": value,
            "weight": round(weight, 2),
            "volatility": round(vol, 4)
        })

    return positions