from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.user import register_user, login_user
from utils.db import load_accounts, save_password_to_db, update_password_in_db, delete_password_from_db  # New methods for update and delete
from utils.encryption import create_fernet_key

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

# Route for fetching accounts
@app.route('/accounts', methods=['GET'])
def api_get_accounts():
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username is required!'}), 400

    accounts = load_accounts()
    user_accounts = accounts.get(username, [])
    return jsonify({'success': True, 'accounts': user_accounts})

# Route for saving new password (create)
@app.route('/passwords', methods=['POST'])
def api_save_password():
    data = request.json
    username = data.get('username')
    account_name = data.get('account_name')
    password = data.get('password')

    if not username or not account_name or not password:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400

    # Save the account password
    save_password_to_db(username, account_name, password)

    return jsonify({'success': True, 'message': 'Password saved successfully!'})

# Route for updating password (update)
@app.route('/passwords/<account_name>', methods=['PUT'])
def api_update_password(account_name):
    data = request.json
    username = data.get('username')
    new_password = data.get('password')

    if not username or not new_password:
        return jsonify({'success': False, 'message': 'Username and new password are required!'}), 400

    # Update the password in the database
    update_password_in_db(username, account_name, new_password)

    return jsonify({'success': True, 'message': 'Password updated successfully!'})

# Route for deleting a password (delete)
@app.route('/passwords/<account_name>', methods=['DELETE'])
def api_delete_password(account_name):
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'success': False, 'message': 'Username is required!'}), 400

    # Delete the account from the database
    delete_password_from_db(username, account_name)

    return jsonify({'success': True, 'message': 'Password deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)