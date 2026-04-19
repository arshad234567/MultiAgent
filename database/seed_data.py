from database.db import get_connection

def save_market_data(df):
    conn = get_connection()
    df.reset_index().to_sql("market_data", conn, if_exists="replace", index=False)
    conn.close()