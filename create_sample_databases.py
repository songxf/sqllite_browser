from datetime import datetime, timedelta
import os

# Import create_sample_database from app.py
from app import create_sample_database

# Configuration
DATABASE_DIR = os.getenv('DATABASE_DIR', '/Users/xsong/Documents/examples/sqllite_browser/databases')
os.makedirs(DATABASE_DIR, exist_ok=True)

# Create databases for the last 7 days
days = 7
start_date = datetime.now() - timedelta(days=days)

for i in range(days):
    date = start_date + timedelta(days=i)
    print(f"Creating database for {date.strftime('%Y-%m-%d')}")
    try:
        create_sample_database(date.year, date.month, date.day)
        print(f"Successfully created database for {date.strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"Error creating database for {date.strftime('%Y-%m-%d')}: {str(e)}")

print("\nDatabase creation complete!")
