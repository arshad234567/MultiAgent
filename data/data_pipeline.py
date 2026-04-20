from database.load_data import load_market_data
from data.generate_positions import generate_positions
from data.generate_limits import get_limits
from services.breach_detector import detect_breach

from agents.reasoning_agent import reasoning_agent
from agents.reporting_agent import reporting_agent, format_report

import requests


def warmup():
    try:
        requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi", "prompt": "hi", "stream": False},
            timeout=5
        )
        print("Ollama warmed up")
    except:
        print("Ollama not responding")


def run():
    symbols = ["AAPL", "MSFT", "GOOG", "TSLA"]

    warmup()

    data = load_market_data()
    data.set_index("Date", inplace=True)

    limits = get_limits()
    latest_prices = data.iloc[-1].to_dict()

    positions = generate_positions(symbols, latest_prices, limits, {})

    breaches = detect_breach(positions, limits)

    print("\n Positions:")
    for p in positions:
        print(p)

    print("\n Breaches:")
    print(breaches)

    print("\n Reasoning + Reports:")

    breaches = sorted(breaches, key=lambda x: x["breach_pct"], reverse=True)

    for breach in breaches:
        pos = next(p for p in positions if p["symbol"] == breach["symbol"])

        analysis = reasoning_agent(breach, pos)
        report = reporting_agent(breach, pos, analysis)

        print("\n" + format_report(breach, analysis, report))


if __name__ == "__main__":
    run()