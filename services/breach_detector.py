def detect_breach(positions, latest_prices, limits):
    breaches = []

    for pos in positions:
        symbol = pos["symbol"]
        value = pos["quantity"] * latest_prices[symbol]

        if value > limits[symbol]:
            breaches.append({
                "symbol": symbol,
                "value": value,
                "limit": limits[symbol],
                "breach_pct": ((value - limits[symbol]) / limits[symbol]) * 100
            })

    return breaches