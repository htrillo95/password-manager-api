import os
import json
from utils.encryption import create_fernet_key  # Import encryption utility

# Define the file path for passwords.json
PASSWORDS_FILE = os.path.join(os.path.dirname(__file__), "passwords.json")

# Load accounts from passwords.json
def load_accounts():
    """Load and return all account data from the passwords.json file."""
    if os.path.exists(PASSWORDS_FILE):
        try:
            with open(PASSWORDS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {PASSWORDS_FILE}: {e}")
            return {}
    return {}

# Save all accounts to passwords.json
def save_accounts(accounts):
    """Save the updated accounts dictionary to passwords.json."""
    try:
        print(f"Saving accounts: {accounts}")  # Debug: Print what is being saved
        with open(PASSWORDS_FILE, "w") as file:
            json.dump(accounts, file, indent=4)
        print(f"Accounts saved successfully: {accounts}")
    except Exception as e:
        print(f"Error saving accounts to {PASSWORDS_FILE}: {e}")

# Add a new account for a user
def save_account(username, account_name, password):
    """Add a new account for a specific user with encryption."""
    print(f"Saving account for {username} - {account_name}...")
    accounts = load_accounts()
    print(f"Current accounts: {accounts}")
    
    if username not in accounts:
        accounts[username] = {"passwords": []}

    # Encrypt the password
    fernet = create_fernet_key()
    encrypted_password = fernet.encrypt(password.encode()).decode()

    # Append the new account
    accounts[username]["passwords"].append({"account_name": account_name, "password": encrypted_password})
    print(f"Updated accounts: {accounts}")
    save_accounts(accounts)

# Update an existing account
def update_account(username, account_name, new_password):
    """Update the password for a specific account under the given username."""
    print(f"Updating account for {username} - {account_name}...")
    accounts = load_accounts()
    print(f"Current accounts before update: {accounts}")

    if username in accounts:
        for account in accounts[username].get("passwords", []):
            if account["account_name"] == account_name:
                fernet = create_fernet_key()
                account["password"] = fernet.encrypt(new_password.encode()).decode()  # Encrypt new password
                print(f"Account updated: {account}")
                save_accounts(accounts)
                return
    print(f"Account {account_name} not found for user {username}.")

# Delete an account
def delete_account(username, account_name):
    """Delete the specified account for a user."""
    print(f"Deleting account for {username} - {account_name}...")
    accounts = load_accounts()
    print(f"Current accounts before deletion: {accounts}")

    if username in accounts:
        accounts[username]["passwords"] = [
            account for account in accounts[username].get("passwords", [])
            if account["account_name"] != account_name
        ]
        print(f"Updated accounts after deletion: {accounts}")
        save_accounts(accounts)
    else:
        print(f"User {username} not found.")