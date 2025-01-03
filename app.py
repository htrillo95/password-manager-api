from flask import Flask, request, jsonify
import os
import json
from cryptography.fernet import Fernet
import bcrypt

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Password Manager API!'

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

@app.route('/register', methods=['POST'])
def api_register_user():
    data = request.json
    username = data['username']
    master_password = data['password']
    users = load_users()
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists!'}), 400
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)
    return jsonify({'success': True, 'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def api_login_user():
    data = request.json
    username = data['username']
    master_password = data['password']
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'message': 'Username not found!'}), 400
    hashed_password = users[username].encode()
    if bcrypt.checkpw(master_password.encode(), hashed_password):
        return jsonify({'success': True, 'message': 'Login successful!'})
    return jsonify({'success': False, 'message': 'Incorrect password!'}), 400

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

if __name__ == '__main__':
    app.run(debug=True)