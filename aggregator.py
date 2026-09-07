import sqlite3
import pandas as pd
import time

def aggregate_sales():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_summary_minute (
            minute_ts TEXT PRIMARY KEY,
            total_sales INTEGER NOT NULL,
            total_revenue REAL NOT NULL
        )
    ''')
    
    # Read raw sales into Pandas
    df = pd.read_sql("SELECT event_ts, amount FROM sales_events", conn)
    
    if not df.empty:
        df['event_ts'] = pd.to_datetime(df['event_ts'])
        df['minute_ts'] = df['event_ts'].dt.strftime('%Y-%m-%d %H:%M:00')
        
        # Aggregate per minute
        summary = df.groupby('minute_ts').agg(
            total_sales=('amount', 'count'),
            total_revenue=('amount', 'sum')
        ).reset_index()
        
        # Save to summary table
        for _, row in summary.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO sales_summary_minute (minute_ts, total_sales, total_revenue)
                VALUES (?, ?, ?)
            ''', (row['minute_ts'], int(row['total_sales']), float(row['total_revenue'])))
            
        conn.commit()
        print(f"Aggregated {len(summary)} minute records.")
        
    conn.close()

if __name__ == "__main__":
    print("Aggregator starting... Updating metrics every 5 seconds.")
    while True:
        aggregate_sales()
        time.sleep(5)