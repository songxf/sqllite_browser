from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import sqlparse
from pathlib import Path
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Configuration
DATABASE_DIR = os.getenv('DATABASE_DIR', '/Users/xsong/Documents/examples/sqllite_browser/databases')

# Ensure database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

def create_sample_database(year, month, day):
    """Create a sample database with test data"""
    date = datetime(year, month, day)
    date_dir = os.path.join(DATABASE_DIR, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), 'refdata')
    os.makedirs(date_dir, exist_ok=True)
    db_path = os.path.join(date_dir, 'refdata.db')
    
    # Check if database already exists and has data
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type="table" AND name="users"')
        has_users = cursor.fetchone()[0] > 0
        conn.close()
        
        if has_users:
            return db_path
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create sample tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample data
    users = [
        ('John Doe', f'john.doe.{year}{month}{day}@example.com'),
        ('Jane Smith', f'jane.smith.{year}{month}{day}@example.com'),
        ('Bob Johnson', f'bob.johnson.{year}{month}{day}@example.com')
    ]
    
    for name, email in users:
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        user_id = cursor.lastrowid
        
        # Add some sample orders
        for _ in range(random.randint(1, 3)):
            cursor.execute('''
                INSERT INTO orders (user_id, amount, status)
                VALUES (?, ?, ?)
            ''', (user_id, round(random.uniform(10, 1000), 2), random.choice(['pending', 'completed', 'cancelled'])))
    
    conn.commit()
    conn.close()
    return db_path

def get_database_hierarchy():
    """Get hierarchical structure of databases"""
    hierarchy = {}
    
    for year in sorted(os.listdir(DATABASE_DIR)):
        if not year.isdigit():
            continue
            
        year_path = os.path.join(DATABASE_DIR, year)
        if not os.path.isdir(year_path):
            continue
            
        hierarchy[year] = {}
        
        for month in sorted(os.listdir(year_path)):
            if not month.isdigit():
                continue
                
            month_path = os.path.join(year_path, month)
            if not os.path.isdir(month_path):
                continue
                
            hierarchy[year][month] = {}
            
            for day in sorted(os.listdir(month_path)):
                if not day.isdigit():
                    continue
                    
                day_path = os.path.join(month_path, day)
                if not os.path.isdir(day_path):
                    continue
                    
                refdata_path = os.path.join(day_path, 'refdata')
                if not os.path.isdir(refdata_path):
                    continue
                    
                db_path = os.path.join(refdata_path, 'refdata.db')
                if os.path.exists(db_path):
                    hierarchy[year][month][day] = db_path
    
    return hierarchy

def get_database_path(year, month, day):
    """Get the path to a database based on date"""
    date = datetime(year, month, day)
    return os.path.join(DATABASE_DIR, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), 'refdata', 'refdata.db')

def get_databases():
    """Get list of all SQLite databases in the database directory"""
    hierarchy = get_database_hierarchy()
    return [f"{year}/{month}/{day}" for year in hierarchy.keys()
                                for month in hierarchy[year].keys()
                                for day in hierarchy[year][month].keys()]

def execute_sql(db_path, sql):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Format SQL for better readability
        formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        
        cursor.execute(formatted_sql)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Get results
        results = cursor.fetchall()
        
        conn.close()
        
        return {
            'success': True,
            'columns': columns,
            'results': results,
            'formatted_sql': formatted_sql
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    databases = get_databases()
    return render_template('index.html', databases=databases)

@app.route('/tables/<int:year>/<int:month>/<int:day>')
def get_tables(year, month, day):
    db_path = get_database_path(year, month, day)
    if not os.path.exists(db_path):
        return jsonify({'error': 'Database not found'}), 404
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/table/<table_name>/<int:year>/<int:month>/<int:day>')
def get_table_data(table_name, year, month, day):
    db_path = get_database_path(year, month, day)
    if not os.path.exists(db_path):
        return jsonify({'error': 'Database not found'}), 404
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        conn.close()
        return jsonify({
            'columns': columns,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute', methods=['POST'])
def execute_query():
    data = request.get_json()
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    sql = data.get('sql')
    
    if not all([year, month, day]):
        return jsonify({'error': 'Date parameters are required'}), 400
    
    db_path = get_database_path(year, month, day)
    if not os.path.exists(db_path):
        return jsonify({'error': 'Database not found'}), 404
    
    result = execute_sql(db_path, sql)
    return jsonify(result)

if __name__ == '__main__':
    # For production, use gunicorn or another production WSGI server
    # This is just for local development
    app.run(host='0.0.0.0', port=5002, debug=False)
