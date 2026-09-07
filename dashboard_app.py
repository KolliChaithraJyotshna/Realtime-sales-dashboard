import streamlit as st
import pandas as pd
import sqlite3
from streamlit_autorefresh import st_autorefresh

def get_summary():
    conn = sqlite3.connect('sales.db')
    df = pd.read_sql("SELECT * FROM sales_summary_minute ORDER BY minute_ts DESC LIMIT 240", conn)
    conn.close()
    return df

st.title("Real-Time Sales Dashboard")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, limit=0, key="refresh")

df = get_summary()

if df.empty:
    st.warning("No sales data yet. Please make sure producer.py is running!")
else:
    latest_revenue = df.iloc[0]['total_revenue']
    st.metric("Revenue (Latest Minute)", f"${latest_revenue:,.2f}")
    
    st.subheader("Revenue Over Time")
    st.line_chart(df.set_index('minute_ts')['total_revenue'])
    
    st.subheader("Recent Minutes Data")
    st.dataframe(df.head(20))