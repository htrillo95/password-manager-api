import json
import os

# Reorganize users.json
def pretty_print_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            data = json.load(file)

        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)

# Reorganize passwords.json
def pretty_print_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)

        with open("passwords.json", "w") as file:
            json.dump(data, file, indent=4)

# Run both to reorganize the files
pretty_print_users()
pretty_print_passwords()