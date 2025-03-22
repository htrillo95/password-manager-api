# utils/sqlite_user.py

import sqlite3
import bcrypt
from utils.sqlite_db import get_db_connection

# Register user
def register_user(data):
    username = data['username']
    master_password = data['password']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return {'success': False, 'message': 'Username already exists!'}

    # Hash the password and insert
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    return {'success': True, 'message': 'User registered successfully!'}


# Login user
def login_user(data):
    username = data['username']
    master_password = data['password']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(master_password.encode(), result['password']):
        return {'success': True, 'message': 'Login successful!'}
    
    return {'success': False, 'message': 'Invalid credentials!'}


# Delete user and their passwords
def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete user’s passwords first (due to foreign key)
    cursor.execute("DELETE FROM passwords WHERE username = ?", (username,))
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return {'success': True, 'message': 'User deleted successfully!'}