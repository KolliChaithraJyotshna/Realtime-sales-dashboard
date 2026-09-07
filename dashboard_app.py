import sqlite3
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, key="datarefresh")

def get_summary():
    conn = sqlite3.connect("sales.db")
    
    # Ensure table exists so Streamlit Cloud does not crash
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales_summary_minute (
            minute_ts TEXT PRIMARY KEY,
            total_sales REAL,
            transaction_count INTEGER
        )
    """)
    
    df = pd.read_sql("SELECT * FROM sales_summary_minute ORDER BY minute_ts DESC LIMIT 240", conn)
    conn.close()
    return df

st.title("Real-Time Sales Dashboard")

df = get_summary()

if df.empty:
    st.info("No sales data available yet. Run your local producer & aggregator scripts to populate data!")
else:
    st.dataframe(df)