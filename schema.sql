CREATE TABLE IF NOT EXISTS sales_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_ts TIMESTAMP NOT NULL,
    order_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    product_category TEXT NOT NULL,
    amount REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS sales_summary_minute (
    minute_ts TEXT PRIMARY KEY,
    total_sales INTEGER NOT NULL,
    total_revenue REAL NOT NULL
);