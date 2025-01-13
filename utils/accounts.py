import json

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_account(username, account_name, password):
    accounts = load_accounts()
    
    if username not in accounts:
        accounts[username] = {}

    if "accounts" not in accounts[username]:
        accounts[username]["accounts"] = []
    
    # Add the new account
    accounts[username]["accounts"].append({"account_name": account_name, "password": password})
    
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)