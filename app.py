from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.user import register_user, login_user
from utils.db import load_accounts, save_password_to_db  # New function for saving password
from utils.encryption import create_fernet_key

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

# New route for saving passwords
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


if __name__ == '__main__':
    app.run(debug=True)