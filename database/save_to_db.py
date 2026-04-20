import sqlite3
import pandas as pd


def save_prices_to_db():
    conn = sqlite3.connect("data_store/risk.db")

    df = pd.read_csv("data_store/processed/prices.csv")

    df.to_sql("market_data", conn, if_exists="replace", index=False)

    conn.close()

    print("Saved market_data to DB")


if __name__ == "__main__":
    save_prices_to_db()