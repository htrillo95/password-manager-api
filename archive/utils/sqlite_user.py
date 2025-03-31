# utils/sqlite_user.py

import bcrypt
from utils.postgres_db import get_db_connection

# Register user
def register_user(data):
    username = data['username']
    master_password = data['password']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        conn.close()
        return {'success': False, 'message': 'Username already exists!'}

    # Hash the password and insert (decode to store as string)
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    conn.close()
    return {'success': True, 'message': 'User registered successfully!'}


# Login user
def login_user(data):
    username = data['username']
    master_password = data['password']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(master_password.encode(), result['password'].encode()):
        return {'success': True, 'message': 'Login successful!'}

    return {'success': False, 'message': 'Invalid credentials!'}


# Delete user and their passwords
def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete user’s passwords first (due to foreign key)
    cursor.execute("DELETE FROM passwords WHERE username = %s", (username,))
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    conn.close()
    return {'success': True, 'message': 'User deleted successfully!'}