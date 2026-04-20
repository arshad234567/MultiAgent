def detect_breach(positions, limits):
    breaches = []

    for pos in positions:
        symbol = pos["symbol"]
        value = pos["value"]
        limit = limits[symbol]

        if value > limit:
            breach_pct = ((value - limit) / limit) * 100

            breaches.append({
                "symbol": symbol,
                "value": value,
                "limit": limit,
                "breach_pct": round(breach_pct, 2)
            })

    return breaches