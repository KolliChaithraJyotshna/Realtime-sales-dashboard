import sqlite3
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Auto-refresh the dashboard every 5 seconds
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
    
    # Insert sample data if empty so the cloud app shows data immediately
    if df.empty:
        sample_data = [
            ("2026-03-07 10:00", 250.50, 5),
            ("2026-03-07 10:01", 410.00, 8),
            ("2026-03-07 10:02", 180.25, 3),
            ("2026-03-07 10:03", 520.75, 10),
            ("2026-03-07 10:04", 310.00, 6),
        ]
        conn.executemany("INSERT OR IGNORE INTO sales_summary_minute VALUES (?, ?, ?)", sample_data)
        conn.commit()
        df = pd.read_sql("SELECT * FROM sales_summary_minute ORDER BY minute_ts DESC LIMIT 240", conn)
        
    conn.close()
    return df

st.title("Real-Time Sales Dashboard")

df = get_summary()

if df.empty:
    st.info("No sales data available yet. Run your local producer & aggregator scripts to populate data!")
else:
    # Display Key Metrics
    total_revenue = df["total_sales"].sum()
    total_transactions = df["transaction_count"].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Total Revenue ($)", f"${total_revenue:,.2f}")
    col2.metric("Total Transactions", f"{total_transactions:,}")
    
    # Display Line Chart
    st.subheader("Sales Trend (Per Minute)")
    chart_df = df.sort_values("minute_ts").set_index("minute_ts")[["total_sales"]]
    st.line_chart(chart_df)

    # Display Data Table
    st.subheader("Recent Sales Summary Data")
    st.dataframe(df)