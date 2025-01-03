from flask import Flask, request, jsonify
import os
import json
from cryptography.fernet import Fernet
import bcrypt

# File paths
USER_FILE = "users.json"
PASSWORDS_FILE = "passwords.json"

# Generate or load an encryption key
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return key

# Initialize encryption
key = load_key()
fernet = Fernet(key)

# Helper functions
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def register_user(username, master_password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)
    return True, "User registered successfully!"

def login_user(username, master_password):
    users = load_users()
    if username not in users:
        return False, "Username not found!"
    hashed_password = users[username].encode()
    if bcrypt.checkpw(master_password.encode(), hashed_password):
        return True, "Login successful!"
    return False, "Incorrect password!"

def load_passwords(username):
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as file:
            data = json.load(file)
            return data.get(username, {})
    return {}

def save_passwords(username, passwords):
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {}
    data[username] = passwords
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(data, file)

def add_password(username, account, password):
    passwords = load_passwords(username)
    encrypted_password = fernet.encrypt(password.encode()).decode()
    passwords[account] = encrypted_password
    save_passwords(username, passwords)

def retrieve_password(username, account):
    passwords = load_passwords(username)
    if account in passwords:
        encrypted_password = passwords[account]
        return fernet.decrypt(encrypted_password.encode()).decode()
    return "Account not found!"

# Flask app
app = Flask(__name__)

@app.route('/register', methods=['POST'])
def api_register_user():
    data = request.json
    username = data['username']
    master_password = data['password']
    success, message = register_user(username, master_password)
    return jsonify({'success': success, 'message': message}), (200 if success else 400)

@app.route('/login', methods=['POST'])
def api_login_user():
    data = request.json
    username = data['username']
    master_password = data['password']
    success, message = login_user(username, master_password)
    return jsonify({'success': success, 'message': message}), (200 if success else 400)

@app.route('/passwords', methods=['POST'])
def api_add_password():
    data = request.json
    username = data['username']
    account = data['account']
    password = data['password']
    add_password(username, account, password)
    return jsonify({'message': 'Password added successfully!'})

@app.route('/passwords', methods=['GET'])
def api_retrieve_password():
    username = request.args.get('username')
    account = request.args.get('account')
    password = retrieve_password(username, account)
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)