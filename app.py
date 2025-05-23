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
    
    # Only create database if it doesn't exist
    if not os.path.exists(db_path):
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
        conn.commit()
        conn.close()
    
    # Always insert sample data regardless of database existence
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert sample data (always insert regardless of existing data)
    users = [
        ('John Doe', f'john.doe.{year}{month}{day}@example.com'),
        ('Jane Smith', f'jane.smith.{year}{month}{day}@example.com'),
        ('Bob Johnson', f'bob.johnson.{year}{month}{day}@example.com'),
        ('Alice Brown', f'alice.brown.{year}{month}{day}@example.com'),
        ('Mike Wilson', f'mike.wilson.{year}{month}{day}@example.com'),
        ('Sarah Thompson', f'sarah.thompson.{year}{month}{day}@example.com'),
        ('David Garcia', f'david.garcia.{year}{month}{day}@example.com'),
        ('Emily Martinez', f'emily.martinez.{year}{month}{day}@example.com'),
        ('Kevin Rodriguez', f'kevin.rodriguez.{year}{month}{day}@example.com'),
        ('Laura Hernandez', f'laura.hernandez.{year}{month}{day}@example.com'),
        ('Thomas Anderson', f'thomas.anderson.{year}{month}{day}@example.com'),
        ('Michelle Chen', f'michelle.chen.{year}{month}{day}@example.com'),
        ('William Turner', f'william.turner.{year}{month}{day}@example.com'),
        ('Rachel Green', f'rachel.green.{year}{month}{day}@example.com'),
        ('James Wilson', f'james.wilson.{year}{month}{day}@example.com'),
        ('Olivia Martinez', f'olivia.martinez.{year}{month}{day}@example.com'),
        ('Daniel Brown', f'daniel.brown.{year}{month}{day}@example.com'),
        ('Sophia Johnson', f'sophia.johnson.{year}{month}{day}@example.com'),
        ('Christopher Lee', f'christopher.lee.{year}{month}{day}@example.com'),
        ('Emma Davis', f'emma.davis.{year}{month}{day}@example.com'),
        ('Michael Thompson', f'michael.thompson.{year}{month}{day}@example.com'),
        ('Grace Rodriguez', f'grace.rodriguez.{year}{month}{day}@example.com'),
        ('Nicholas Hernandez', f'nicholas.hernandez.{year}{month}{day}@example.com'),
        ('Victoria Martinez', f'victoria.martinez.{year}{month}{day}@example.com'),
        ('Joseph Wilson', f'joseph.wilson.{year}{month}{day}@example.com'),
        ('Elizabeth Brown', f'elizabeth.brown.{year}{month}{day}@example.com'),
        ('Matthew Johnson', f'matthew.johnson.{year}{month}{day}@example.com'),
        ('Laura Garcia', f'laura.garcia.{year}{month}{day}@example.com'),
        ('David Rodriguez', f'david.rodriguez.{year}{month}{day}@example.com'),
        ('Jessica Hernandez', f'jessica.hernandez.{year}{month}{day}@example.com')
    ]
    
    # Add unique index to emails
    for i, (name, email) in enumerate(users):
        base_email = email.split('@')[0]
        users[i] = (name, f'{base_email}.{i}@example.com')
    
    for name, email in users:
        try:
            cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            user_id = cursor.lastrowid
            
            # Add more sample orders with varied data
            for _ in range(random.randint(3, 6)):
                status = random.choice(['pending', 'completed', 'cancelled', 'shipped', 'delivered'])
                amount = round(random.uniform(10, 2000), 2)
                
                cursor.execute('''
                    INSERT INTO orders (user_id, amount, status)
                    VALUES (?, ?, ?)
                ''', (user_id, amount, status))
        except sqlite3.IntegrityError:
            # Skip if user already exists (due to UNIQUE constraint on email)
            continue
    
    # Insert more diverse sample data
    users = [
        ('John Doe', f'john.doe.{year}{month}{day}@example.com'),
        ('Jane Smith', f'jane.smith.{year}{month}{day}@example.com'),
        ('Bob Johnson', f'bob.johnson.{year}{month}{day}@example.com'),
        ('Alice Brown', f'alice.brown.{year}{month}{day}@example.com'),
        ('Mike Wilson', f'mike.wilson.{year}{month}{day}@example.com'),
        ('Sarah Thompson', f'sarah.thompson.{year}{month}{day}@example.com'),
        ('David Garcia', f'david.garcia.{year}{month}{day}@example.com'),
        ('Emily Martinez', f'emily.martinez.{year}{month}{day}@example.com'),
        ('Kevin Rodriguez', f'kevin.rodriguez.{year}{month}{day}@example.com'),
        ('Laura Hernandez', f'laura.hernandez.{year}{month}{day}@example.com'),
        ('Thomas Anderson', f'thomas.anderson.{year}{month}{day}@example.com'),
        ('Michelle Chen', f'michelle.chen.{year}{month}{day}@example.com'),
        ('William Turner', f'william.turner.{year}{month}{day}@example.com'),
        ('Rachel Green', f'rachel.green.{year}{month}{day}@example.com'),
        ('James Wilson', f'james.wilson.{year}{month}{day}@example.com'),
        ('Olivia Martinez', f'olivia.martinez.{year}{month}{day}@example.com'),
        ('Daniel Brown', f'daniel.brown.{year}{month}{day}@example.com'),
        ('Sophia Johnson', f'sophia.johnson.{year}{month}{day}@example.com'),
        ('Christopher Lee', f'christopher.lee.{year}{month}{day}@example.com'),
        ('Emma Davis', f'emma.davis.{year}{month}{day}@example.com'),
        ('Michael Thompson', f'michael.thompson.{year}{month}{day}@example.com'),
        ('Grace Rodriguez', f'grace.rodriguez.{year}{month}{day}@example.com'),
        ('Nicholas Hernandez', f'nicholas.hernandez.{year}{month}{day}@example.com'),
        ('Victoria Martinez', f'victoria.martinez.{year}{month}{day}@example.com'),
        ('Joseph Wilson', f'joseph.wilson.{year}{month}{day}@example.com'),
        ('Elizabeth Brown', f'elizabeth.brown.{year}{month}{day}@example.com'),
        ('Matthew Johnson', f'matthew.johnson.{year}{month}{day}@example.com'),
        ('Laura Garcia', f'laura.garcia.{year}{month}{day}@example.com'),
        ('David Rodriguez', f'david.rodriguez.{year}{month}{day}@example.com'),
        ('Jessica Hernandez', f'jessica.hernandez.{year}{month}{day}@example.com')
    ]
    
    for name, email in users:
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        user_id = cursor.lastrowid
        
        # Add more sample orders with varied data
        for _ in range(random.randint(3, 6)):
            status = random.choice(['pending', 'completed', 'cancelled', 'shipped', 'delivered'])
            amount = round(random.uniform(10, 2000), 2)
            
            cursor.execute('''
                INSERT INTO orders (user_id, amount, status)
                VALUES (?, ?, ?)
            ''', (user_id, amount, status))
    
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
    """Get the path to a database based on date, creating it if it doesn't exist"""
    date = datetime(year, month, day)
    db_path = os.path.join(DATABASE_DIR, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), 'refdata', 'refdata.db')
    
    # Create the database if it doesn't exist
    if not os.path.exists(db_path):
        create_sample_database(year, month, day)
    
    return db_path

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
        
        # Execute the SQL
        cursor.execute(sql)
        
        # If it's a SELECT query, get results
        if sql.strip().upper().startswith('SELECT'):
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            conn.commit()
            conn.close()
            return {
                'columns': columns,
                'results': results,
                'formatted_sql': formatted_sql
            }
        else:
            # For non-SELECT queries (INSERT, UPDATE, DELETE)
            conn.commit()
            conn.close()
            return {
                'formatted_sql': formatted_sql,
                'message': 'Query executed successfully'
            }
    except Exception as e:
        conn.rollback()
        conn.close()
        return {'error': str(e)}

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
    """Get paginated data from a specific table"""
    # Get pagination parameters from request args
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    db_path = get_database_path(year, month, day)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get total count
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        total = cursor.fetchone()[0]
        
        # Get paginated data with proper SQL escaping
        offset = (page - 1) * per_page
        query = f'SELECT * FROM {table_name} LIMIT ? OFFSET ?'
        cursor.execute(query, (per_page, offset))
        results = cursor.fetchall()
        
        conn.close()
        
        # Generate SQL query for viewing table data
        sql_query = f"SELECT * FROM {table_name} LIMIT {per_page} OFFSET {offset}"
        formatted_sql = sqlparse.format(sql_query, reindent=True, keyword_case='upper')
        
        return jsonify({
            'columns': columns,
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'formatted_sql': formatted_sql
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute', methods=['POST'])
def execute_query():
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Get required parameters
        year_str = data.get('year')
        month_str = data.get('month')
        day_str = data.get('day')
        sql = data.get('sql')
        
        if not all([year_str, month_str, day_str]):
            return jsonify({'error': 'Date parameters are required'}), 400
            
        try:
            # Convert string parameters to integers
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)
            
            # Validate date range
            if not (1 <= month <= 12) or not (1 <= day <= 31):
                return jsonify({'error': 'Invalid date parameters'}), 400
                
        except ValueError:
            return jsonify({'error': 'Date parameters must be valid numbers'}), 400
            
        db_path = get_database_path(year, month, day)
        if not os.path.exists(db_path):
            return jsonify({'error': 'Database not found'}), 404
            
        result = execute_sql(db_path, sql)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For production, use gunicorn or another production WSGI server
    # This is just for local development
    app.run(host='0.0.0.0', port=5002, debug=True)
