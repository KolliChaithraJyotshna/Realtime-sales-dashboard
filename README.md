# Real-Time Sales Dashboard

🚀 **Live Demo:** [View Live Streamlit Dashboard](https://realtime-sales-dashboard-8fxljp2acqp5bayfd8rkmd.streamlit.app/)

A real-time data streaming and visualization pipeline built with Python, SQLite, Pandas, and Streamlit.

## Architecture
- **producer.py**: Generates synthetic real-time sales transactions.
- **aggregator.py**: ETL process that aggregates raw sales into per-minute summaries.
- **sales.db**: Local SQLite database for persistent storage.
- **dashboard_app.py**: Live auto-refreshing Streamlit dashboard.
## How to Run

### Standard Setup
1. Run producer: `python producer.py`
2. Run aggregator: `python aggregator.py`
3. Start dashboard: `streamlit run dashboard_app.py`

### Windows / Anaconda (if `python` is not in PATH)
If `python` is not recognized in your terminal, run using your Anaconda binary path:
1. `& "C:\Users\chait\anaconda3\python.exe" producer.py`
2. `& "C:\Users\chait\anaconda3\python.exe" aggregator.py`
3. `& "C:\Users\chait\anaconda3\python.exe" -m streamlit run dashboard_app.py`
