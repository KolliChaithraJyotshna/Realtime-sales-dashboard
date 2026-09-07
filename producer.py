import time
import uuid
import random
import sqlite3
from datetime import datetime

CATEGORIES = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']

def init_db():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_ts TIMESTAMP NOT NULL,
            order_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            product_category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_sale():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    
    event_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_id = str(uuid.uuid4())[:8]
    user_id = f"user_{random.randint(100, 999)}"
    category = random.choice(CATEGORIES)
    amount = round(random.uniform(10.0, 500.0), 2)
    
    cursor.execute('''
        INSERT INTO sales_events (event_ts, order_id, user_id, product_category, amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (event_ts, order_id, user_id, category, amount))
    
    conn.commit()
    conn.close()
    print(f"[{event_ts}] Generated Sale: ${amount:.2f} ({category})")

if __name__ == "__main__":
    init_db()
    print("Producer starting... Generating sales data every 2 seconds.")
    while True:
        generate_sale()
        time.sleep(2)