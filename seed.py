# Connect to MySQL server:

import mysql.connector
import uuid
import csv

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password"
    )

# Create database:

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()


# Connect to ALX_prodev database:

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )


# Create table user_data:

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data(
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """)
    cursor.close()
    print("Table user_data created successfully")

# Insert data from CSV:

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
            INSERT IGNORE INTO user_data(user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
