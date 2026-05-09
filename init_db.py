"""
Database initialization script
Run this first to create database and tables
"""

import sqlite3
import hashlib
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and sample data"""
    
    # Connect to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    
    # Create admin user (password: admin123)
    admin_password = generate_password_hash('admin123')
    try:
        cursor.execute('''
            INSERT INTO users (username, password, role) 
            VALUES (?, ?, ?)
        ''', ('admin', admin_password, 'admin'))
        print("Admin user created successfully!")
    except sqlite3.IntegrityError:
        print("Admin user already exists")
    
    # Create sample users
    user_password = generate_password_hash('user123')
    try:
        cursor.execute(''')
            INSERT INTO users (username, password, role) 
            VALUES (?, ?, ?)
        ''', ('user1', user_password, 'user'))
        print("Sample user created successfully!")
    except sqlite3.IntegrityError:
        print("Sample user already exists")
    
    # Insert sample students
    sample_students = [
        ('John Doe', 'john@example.com', 'Computer Science'),
        ('Jane Smith', 'jane@example.com', 'Mathematics'),
        ('Bob Johnson', 'bob@example.com', 'Physics'),
        ('Alice Brown', 'alice@example.com', 'Chemistry'),
        ('Charlie Wilson', 'charlie@example.com', 'Biology')
    ]
    
    for student in sample_students:
        try:
            cursor.execute('''
                INSERT INTO students (name, email, course) 
                VALUES (?, ?, ?)
            ''', student)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
    print("\nTest Credentials:")
    print("Admin - Username: admin, Password: admin123")
    print("User - Username: user1, Password: user123")

if __name__ == '__main__':
    init_database()
