# 0-databaseconnection.py
import sqlite3

class DatabaseConnection:
    """Class-based context manager to handle DB connections"""
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# Using the context manager
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
