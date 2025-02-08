from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.user import register_user, login_user
from utils.db import load_accounts, save_password_to_db, update_password_in_db, delete_password_from_db
from utils.encryption import create_fernet_key
from utils.db import update_username_in_db 

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

@app.route('/')
def home():
    return 'Welcome to the Password Manager API!'

@app.route('/register', methods=['POST'])
def api_register_user():
    data = request.json
    response = register_user(data)
    return jsonify(response), 400 if not response['success'] else 200

@app.route('/login', methods=['POST'])
def api_login_user():
    data = request.json
    response = login_user(data)
    return jsonify(response), 400 if not response['success'] else 200

# Fetch stored accounts for a user
@app.route('/accounts', methods=['GET'])
def api_get_accounts():
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username is required!'}), 400

    passwords = load_accounts()
    user_data = passwords.get(username, {"passwords": []})
    fernet = create_fernet_key()

    # Decrypt passwords before sending to frontend
    decrypted_accounts = [
        {
            "account_name": account["account_name"],
            "password": fernet.decrypt(account["password"].encode()).decode()
        }
        for account in user_data.get("passwords", [])
    ]

    return jsonify({'success': True, 'accounts': decrypted_accounts})

# Save a new account
@app.route('/passwords', methods=['POST'])
def api_save_password():
    data = request.json
    username = data.get('username')
    account_name = data.get('account_name')
    password = data.get('password')

    if not username or not account_name or not password:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400

    save_password_to_db(username, account_name, password)
    return jsonify({'success': True, 'message': 'Password saved successfully!'})

# Update an existing password
@app.route('/passwords/<account_name>', methods=['PUT'])
def api_update_password(account_name):
    data = request.json
    username = data.get('username')
    new_password = data.get('password')

    if not username or not new_password:
        return jsonify({'success': False, 'message': 'Username and new password are required!'}), 400

    update_password_in_db(username, account_name, new_password)
    return jsonify({'success': True, 'message': 'Password updated successfully!'})

# Delete an account
@app.route('/passwords/<account_name>', methods=['DELETE'])
def api_delete_password(account_name):
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'success': False, 'message': 'Username is required!'}), 400

    delete_password_from_db(username, account_name)
    return jsonify({'success': True, 'message': 'Password deleted successfully!'})

@app.route('/update-username', methods=['PUT'])
def api_update_username():
    data = request.json
    current_username = data.get('current_username')
    new_username = data.get('new_username')

    if not current_username or not new_username:
        return jsonify({'success': False, 'message': 'Both current and new username are required!'}), 400

    response = update_username_in_db(current_username, new_username)
    return jsonify(response), 400 if not response['success'] else 200

if __name__ == '__main__':
    app.run(debug=True)