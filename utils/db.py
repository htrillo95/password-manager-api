import os
import json
from utils.encryption import create_fernet_key  # Use the encryption utility

USER_FILE = "users.json"
PASSWORDS_FILE = "passwords.json"

# Load users from users.json
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to users.json
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Load accounts from passwords.json
def load_accounts():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save password to passwords.json (encrypt password before saving)
def save_password_to_db(username, account_name, password):
    # Get the Fernet encryption instance
    fernet = create_fernet_key()

    # Load existing accounts
    passwords = load_accounts()

    # Initialize user's password list if not already done
    if username not in passwords:
        passwords[username] = {}

    # Encrypt the password
    encrypted_password = fernet.encrypt(password.encode()).decode()

    # Save the encrypted password under the user's account
    if "passwords" not in passwords[username]:
        passwords[username]["passwords"] = []

    passwords[username]["passwords"].append({"account_name": account_name, "password": encrypted_password})

    # Save the updated data to passwords.json
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)