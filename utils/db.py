import os
import json
from utils.encryption import create_fernet_key  # Ensure you have the encryption utility imported

USER_FILE = "users.json"
PASSWORDS_FILE = "passwords.json"

# Load users from users.json
def load_users():
    """Load and return all users from the users.json file."""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to users.json
def save_users(users):
    """Save the updated users dictionary to users.json."""
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Load accounts from passwords.json
def load_accounts():
    """Load and return all account data from the passwords.json file."""
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as file:
            return json.load(file)
    return {}

#Saves updated user account data back to passwords.json after changes
def save_accounts(accounts):
    """Save the updated accounts dictionary to passwords.json."""
    try:
        with open(PASSWORDS_FILE, "w") as file:
            json.dump(accounts, file, indent=4)
        print("✅ Accounts successfully saved to passwords.json")
    except Exception as e:
        print(f"❌ Error saving accounts to {PASSWORDS_FILE}: {e}")

# Save a password to passwords.json (encrypt password before saving)
def save_password_to_db(username, account_name, password):
    """Encrypt and save the account password to passwords.json."""
    fernet = create_fernet_key()  # Get the Fernet encryption instance

    # Load existing account data
    passwords = load_accounts()

    # Initialize user's password list if not already done
    if username not in passwords:
        passwords[username] = {"passwords": []}

    # Encrypt the password
    encrypted_password = fernet.encrypt(password.encode()).decode()  # Encrypt the actual password, not the Fernet object

    # Append the new account password
    passwords[username]["passwords"].append({"account_name": account_name, "password": encrypted_password})

    # Save the updated passwords data back to passwords.json
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# Update an existing password for an account
def update_password_in_db(username, account_name, new_password):
    """Update the password for a specific account under the given username."""
    fernet = create_fernet_key()  # Get the Fernet encryption instance

    # Load existing account data
    passwords = load_accounts()

    # Check if the username exists
    if username in passwords:
        accounts = passwords[username].get("passwords", [])
        
        # Find and update the password for the given account_name
        for account in accounts:
            if account["account_name"] == account_name:
                encrypted_password = fernet.encrypt(new_password.encode('utf-8')).decode()
                account["password"] = encrypted_password  # Update password
                break

    # Save the updated passwords data back to passwords.json
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# Delete an account by name
def delete_password_from_db(username, account_name):
    """Delete the specified account from the passwords list."""
    # Load existing account data
    passwords = load_accounts()

    # Check if the username exists
    if username in passwords:
        accounts = passwords[username].get("passwords", [])

        # Filter out the account to delete
        passwords[username]["passwords"] = [account for account in accounts if account["account_name"] != account_name]

    # Save the updated passwords data back to passwords.json
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# Update username in users.json
def update_username_in_db(current_username, new_username):
    """Update the username in the users.json file."""
    users = load_users()  # Load existing users

    if current_username not in users:
        return {'success': False, 'message': 'Current username not found!'}

    if new_username in users:
        return {'success': False, 'message': 'New username already exists!'}

    # Move the user's data under the new username
    users[new_username] = users.pop(current_username)
    
    # Save updated user data
    save_users(users)

    return {'success': True, 'message': 'Username updated successfully!'}