from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import sqlparse
from pathlib import Path

app = Flask(__name__)

# Configuration
DATABASE_DIR = os.getenv('DATABASE_DIR', '/Users/xsong/Documents/examples/sqllite_browser/databases')

# Ensure database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

def get_databases():
    """Get list of all SQLite databases in the database directory"""
    return [f for f in os.listdir(DATABASE_DIR) if f.endswith('.db')]

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

@app.route('/tables')
def get_tables():
    db_name = request.args.get('db')
    if not db_name:
        return jsonify({'error': 'Database name is required'}), 400
    
    db_path = os.path.join(DATABASE_DIR, db_name)
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

@app.route('/table/<table_name>')
def get_table_data(table_name):
    db_name = request.args.get('db')
    if not db_name:
        return jsonify({'error': 'Database name is required'}), 400
    
    db_path = os.path.join(DATABASE_DIR, db_name)
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
    db_name = data.get('db')
    sql = data.get('sql')
    
    if not db_name or not sql:
        return jsonify({'error': 'Database name and SQL are required'}), 400
    
    db_path = os.path.join(DATABASE_DIR, db_name)
    if not os.path.exists(db_path):
        return jsonify({'error': 'Database not found'}), 404
    
    return jsonify(execute_sql(db_path, sql))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
