import sqlite3
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Import pipeline functions from producer and aggregator
from producer import init_db, generate_sale
from aggregator import aggregate_sales

# Auto-refresh the dashboard every 5 seconds
st_autorefresh(interval=5000, key="datarefresh")

# Trigger background pipeline tasks automatically on each refresh
try:
    init_db()
    generate_sale()
    aggregate_sales()
except Exception as e:
    pass


def get_summary():
    conn = sqlite3.connect("sales.db")

    # Ensure table exists so Streamlit Cloud does not throw an error
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales_summary_minute (
            minute_ts TEXT PRIMARY KEY,
            total_sales INTEGER NOT NULL,
            total_revenue REAL NOT NULL
        )
    """)

    df = pd.read_sql(
        "SELECT * FROM sales_summary_minute ORDER BY minute_ts DESC LIMIT 240",
        conn,
    )

    # Insert initial sample data if table is completely empty on launch
    if df.empty:
        sample_data = [
            ("2026-03-07 10:00", 5, 250.50),
            ("2026-03-07 10:01", 8, 410.00),
            ("2026-03-07 10:02", 3, 180.25),
            ("2026-03-07 10:03", 10, 520.75),
            ("2026-03-07 10:04", 6, 310.00),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO sales_summary_minute VALUES (?, ?, ?)",
            sample_data,
        )
        conn.commit()
        df = pd.read_sql(
            "SELECT * FROM sales_summary_minute ORDER BY minute_ts DESC LIMIT"
            " 240",
            conn,
        )

    conn.close()
    return df


# Main Streamlit UI Setup
st.title("Real-Time Sales Dashboard")

df = get_summary()

if not df.empty:
    # Display Key Metrics
    total_revenue = df["total_revenue"].sum()
    total_transactions = df["total_sales"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Revenue ($)", f"${total_revenue:,.2f}")
    col2.metric("Total Transactions", f"{total_transactions:,}")

    # Display Per-Minute Sales Trend Line Chart
    st.subheader("Sales Trend (Per Minute)")
    chart_df = df.sort_values("minute_ts").set_index("minute_ts")[
        ["total_revenue"]
    ]
    st.line_chart(chart_df)

    # Display Raw Aggregated Data Table
    st.subheader("Recent Sales Summary Data")
    st.dataframe(df)