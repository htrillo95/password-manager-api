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

    # Save the password in the passwords.json
    fernet = create_fernet_key()
    save_password_to_db(username, master_password, fernet)

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