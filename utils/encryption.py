import os
from cryptography.fernet import Fernet

# Function to load or generate a key
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return key

# Function to create Fernet object
def create_fernet_key():
    key = load_key()
    return Fernet(key)