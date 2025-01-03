import os
import json
from cryptography.fernet import Fernet
import bcrypt  # Install with `pip install bcrypt`

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

# User management functions
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
        return "Username already exists!"
    
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)
    return "User registered successfully!"

def login_user(username, master_password):
    users = load_users()
    if username not in users:
        return False, "Username not found!"
    
    hashed_password = users[username].encode()
    if bcrypt.checkpw(master_password.encode(), hashed_password):
        return True, "Login successful!"
    return False, "Incorrect password!"

# Password management functions
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
    return f"Account not found! Stored accounts: {', '.join(passwords.keys()) if passwords else 'None'}"

def list_accounts(username):
    passwords = load_passwords(username)
    if not passwords:
        return "No accounts found!"
    return "\n".join(passwords.keys())

# Main program
if __name__ == "__main__":
    print("Welcome to the Password Manager")
    logged_in_user = None

    while not logged_in_user:
        print("\n[1] Register")
        print("[2] Login")
        choice = input("Choose an option: ")
        
        if choice == "1":
            username = input("Enter a username: ")
            master_password = input("Enter a master password: ")
            print(register_user(username, master_password))
        elif choice == "2":
            username = input("Enter your username: ")
            master_password = input("Enter your master password: ")
            success, message = login_user(username, master_password)
            print(message)
            if success:
                logged_in_user = username
        else:
            print("Invalid choice!")

    print(f"\nWelcome, {logged_in_user}!")
    while True:
        print("\n[1] Add Password")
        print("[2] Retrieve Password")
        print("[3] List All Stored Accounts")
        print("[4] Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            account = input("Account Name: ")
            password = input("Password: ")
            add_password(logged_in_user, account, password)
            print("Password added!")
        elif choice == "2":
            account = input("Account Name: ")
            print(f"Password: {retrieve_password(logged_in_user, account)}")
        elif choice == "3":
            print("Stored Accounts:")
            print(list_accounts(logged_in_user))
        elif choice == "4":
            break
        else:
            print("Invalid choice!")