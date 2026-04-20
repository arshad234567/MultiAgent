import sqlite3
import pandas as pd

def load_market_data():
    conn = sqlite3.connect("data_store/risk.db")
    df = pd.read_sql("SELECT * FROM market_data", conn)
    conn.close()
    return df