# 0-databaseconnection.py
import sqlite3

class DatabaseConnection:
    """Class-based context manager to handle DB connections"""
    
    def __init__(self):
        """Initialize the DatabaseConnection object"""
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Using the context manager
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
