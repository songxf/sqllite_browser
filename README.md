# SQLite Browser

A web-based SQLite database browser built with Python Flask.

## Features

- Browse SQLite databases from a specified directory
- View all tables in a database
- View table contents
- Execute custom SQL queries with auto-formatting
- Modern web interface with Bootstrap

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your database directory path:
```
DATABASE_DIR=/path/to/your/databases
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Select a database from the dropdown
2. View available tables
3. Click "View" to see table contents
4. Use the SQL editor to execute custom queries
5. Results will be displayed in a formatted table

## Note

Make sure the database files are readable by the application. The application will look for SQLite databases in the directory specified by `DATABASE_DIR` environment variable.
