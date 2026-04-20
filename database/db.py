import sqlite3

def get_connection():
    return sqlite3.connect("data/risk.db", timeout=10)