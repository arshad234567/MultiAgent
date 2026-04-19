import random


def generate_positions(symbols):
    positions = []

    for symbol in symbols:
        positions.append({
            "trader_id": f"T{random.randint(100, 999)}",
            "symbol": symbol,
            "quantity": random.randint(100, 5000)
        })

    return positions