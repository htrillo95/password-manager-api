import os
import json
from cryptography.fernet import Fernet

USER_FILE = "users.json"
PASSWORDS_FILE = "passwords.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

def load_accounts():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_passwords(username, password, fernet):
    passwords = load_accounts()

    if username not in passwords:
        passwords[username] = {}

    encrypted_password = fernet.encrypt(password.encode()).decode()

    passwords[username]["passwords"] = passwords[username].get("passwords", []) + [encrypted_password]

    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)