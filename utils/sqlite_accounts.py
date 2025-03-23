# utils/sqlite_accounts.py

import sqlite3
from utils.postgres_db import get_db_connection
from utils.encryption import create_fernet_key

# Save new password
def save_password_to_db(username, account_name, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Encrypt password
    fernet = create_fernet_key()
    encrypted_password = fernet.encrypt(password.encode()).decode()

    # Insert into DB
    cursor.execute("""
        INSERT INTO passwords (username, account_name, password)
        VALUES (%s, %s, %s)
    """, (username, account_name, encrypted_password))

    conn.commit()
    conn.close()


# Update password
def update_password_in_db(username, account_name, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()

    fernet = create_fernet_key()
    encrypted_password = fernet.encrypt(new_password.encode()).decode()

    cursor.execute("""
        UPDATE passwords
        SET password = %s
        WHERE username = %s AND account_name = %s
    """, (encrypted_password, username, account_name))

    conn.commit()
    conn.close()


# Delete password/account
def delete_password_from_db(username, account_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM passwords
        WHERE username = %s AND account_name = %s
    """, (username, account_name))

    conn.commit()
    conn.close()


# Update username across both users and passwords tables
def update_username_in_db(current_username, new_username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if current username exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (current_username,))
    if not cursor.fetchone():
        conn.close()
        return {'success': False, 'message': 'Current username not found!'}

    # Check if new username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
    if cursor.fetchone():
        conn.close()
        return {'success': False, 'message': 'New username already exists! Please choose another one.'}

    # Update username in users table
    cursor.execute("UPDATE users SET username = %s WHERE username = %s", (new_username, current_username))

    # Update username in passwords table
    cursor.execute("UPDATE passwords SET username = %s WHERE username = %s", (new_username, current_username))

    conn.commit()
    conn.close()

    return {'success': True, 'message': 'Username updated successfully!'}