import bcrypt
from utils.db import load_users, save_users, save_password_to_db
from utils.encryption import create_fernet_key
from utils.db import load_accounts, save_accounts
from flask import session

def register_user(data):
    username = data['username']
    master_password = data['password']
    users = load_users()

    if username in users:
        return {'success': False, 'message': 'Username already exists!'}

    # Hash the master password using bcrypt
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)  # Save the updated users.json

    # ✅ Initialize an empty password list for the user in passwords.json
    passwords = load_accounts()
    if username not in passwords:
        passwords[username] = {"passwords": []}  # Create empty password storage
        save_accounts(passwords)  # Save updated passwords.json

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
    # 🔥 Ensure user is logged in
    if "username" not in session:
        return {'success': False, 'message': 'Unauthorized!'}, 401

    old_username = session["username"]  # 🔥 Use the session to get the logged-in user
    new_username = data.get("new_username")
    
    users = load_users()

    if not new_username:
        return {'success': False, 'message': 'New username is required!'}, 400

    if new_username in users:
        return {'success': False, 'message': 'New username is already taken!'}, 409

    # ✅ Update the username in users.json
    users[new_username] = users.pop(old_username)
    save_users(users)

    # ✅ Move stored accounts under the new username
    passwords = load_accounts()
    if old_username in passwords:
        passwords[new_username] = passwords.pop(old_username)
        save_accounts(passwords)  # Save changes to the accounts file

    # ✅ Update session with the new username
    session["username"] = new_username

    return {'success': True, 'message': 'Username updated successfully!'}

# user.py

def delete_user(username):
    """Delete a user and all their stored accounts."""
    users = load_users()
    
    if username not in users:
        return {'success': False, 'message': 'User not found!'}

    # Remove user from users.json
    del users[username]
    save_users(users)

    # Remove user’s stored passwords from passwords.json
    passwords = load_accounts()
    if username in passwords:
        del passwords[username]
        save_accounts(passwords)

    return {'success': True, 'message': 'User account deleted successfully!'}