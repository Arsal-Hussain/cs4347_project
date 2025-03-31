# lib/database.py

import sqlite3

DB_PATH = "db/library.db"

def get_connection():
    """Establish and return a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
