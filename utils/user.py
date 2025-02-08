import bcrypt
from utils.db import load_users, save_users, save_password_to_db
from utils.encryption import create_fernet_key

def register_user(data):
    username = data['username']
    master_password = data['password']
    users = load_users()

    if username in users:
        return {'success': False, 'message': 'Username already exists!'}

    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)

    # Save the password in the passwords.json (encrypt using Fernet)
    fernet = create_fernet_key()
    save_password_to_db(username, master_password, master_password)  # <-- This should pass the password, not fernet

    return {'success': True, 'message': 'User registered successfully!'}

def login_user(data):
    username = data['username']
    master_password = data['password']
    users = load_users()

    if username not in users:
        return {'success': False, 'message': 'Username not found!'}

    hashed_password = users[username].encode()
    if bcrypt.checkpw(master_password.encode(), hashed_password):
        return {'success': True, 'message': 'Login successful!'}

    return {'success': False, 'message': 'Incorrect password!'}

def update_username(data):
    old_username = data.get("old_username")
    new_username = data.get("new_username")
    users = load_users()

    if not old_username or not new_username:
        return {'success': False, 'message': 'Both old and new usernames are required!'}

    if old_username not in users:
        return {'success': False, 'message': 'Old username not found!'}

    if new_username in users:
        return {'success': False, 'message': 'New username is already taken!'}

    # Update the username in the users.json
    users[new_username] = users.pop(old_username)
    save_users(users)

    # Move stored accounts under the new username
    passwords = load_accounts()
    if old_username in passwords:
        passwords[new_username] = passwords.pop(old_username)
        save_password_to_db(new_username, None, None)  # Save changes to the database

    return {'success': True, 'message': 'Username updated successfully!'}