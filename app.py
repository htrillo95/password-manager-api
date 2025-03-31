from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask app running directly without Gunicorn"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from utils.sqlite_db import init_db
# from utils.sqlite_user import register_user, login_user, delete_user
# from utils.sqlite_accounts import save_password_to_db, update_password_in_db, delete_password_from_db, update_username_in_db
# from utils.encryption import create_fernet_key
# from dotenv import load_dotenv
# load_dotenv()

# # ✅ Initialize DB when app starts
# # init_db()



# app = Flask(__name__)
# ######################################
# # CORS(app, origins=[
# #     "http://localhost:3000",
# #     "https://riverlock.vercel.app",
# #     "https://riverlock-p04pj5vsx-hector-ts-projects.vercel.app",
# #     "https://riverlock-jcpb410sb-hector-ts-projects.vercel.app"
# # ], supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type"])
# ######################################

# CORS(app, origins="*", supports_credentials=True,
#      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#      allow_headers=["Content-Type"])

# ################################
# # @app.before_request
# # def handle_options_request():
# #     if request.method == 'OPTIONS':
# #         return '', 200
# ###################################    

# @app.route('/')
# def home():
#     return 'Welcome to the Password Manager API!'

# @app.route('/register', methods=['POST'])
# def api_register_user():
#     data = request.json
#     response = register_user(data)
#     return jsonify(response), 400 if not response['success'] else 200

# @app.route('/login', methods=['POST'])
# def api_login_user():
#     data = request.json
#     response = login_user(data)
#     return jsonify(response), 400 if not response['success'] else 200

# @app.route('/accounts', methods=['GET'])
# def api_get_accounts():
#     from utils.postgres_db import get_db_connection
#     username = request.args.get('username')
#     if not username:
#         return jsonify({'success': False, 'message': 'Username is required!'}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT account_name, password FROM passwords WHERE username = %s", (username,))
#     rows = cursor.fetchall()
#     conn.close()

#     fernet = create_fernet_key()
#     decrypted_accounts = [
#         {
#             "account_name": row["account_name"],
#             "password": fernet.decrypt(row["password"].encode()).decode()
#         }
#         for row in rows
#     ]

#     return jsonify({'success': True, 'accounts': decrypted_accounts})

# @app.route('/passwords', methods=['POST'])
# def api_save_password():
#     data = request.json
#     username = data.get('username')
#     account_name = data.get('account_name')
#     password = data.get('password')

#     if not username or not account_name or not password:
#         return jsonify({'success': False, 'message': 'All fields are required!'}), 400

#     save_password_to_db(username, account_name, password)
#     return jsonify({'success': True, 'message': 'Password saved successfully!'})

# @app.route('/passwords/<account_name>', methods=['PUT'])
# def api_update_password(account_name):
#     data = request.json
#     username = data.get('username')
#     new_password = data.get('password')

#     if not username or not new_password:
#         return jsonify({'success': False, 'message': 'Username and new password are required!'}), 400

#     update_password_in_db(username, account_name, new_password)
#     return jsonify({'success': True, 'message': 'Password updated successfully!'})

# @app.route('/passwords/<account_name>', methods=['DELETE'])
# def api_delete_password(account_name):
#     data = request.json
#     username = data.get('username')

#     if not username:
#         return jsonify({'success': False, 'message': 'Username is required!'}), 400

#     delete_password_from_db(username, account_name)
#     return jsonify({'success': True, 'message': 'Password deleted successfully!'})

# @app.route('/update-username', methods=['PUT'])
# def api_update_username():
#     data = request.json
#     current_username = data.get('current_username')
#     new_username = data.get('new_username')

#     if not current_username or not new_username:
#         return jsonify({'success': False, 'message': 'Both current and new usernames are required!'}), 400

#     response = update_username_in_db(current_username, new_username)

#     if response.get("success"):
#         return jsonify(response), 200
#     else:
#         return jsonify(response), 400

# @app.route('/delete-account', methods=['DELETE'])
# def api_delete_user():
#     data = request.json
#     username = data.get('username')

#     if not username:
#         return jsonify({'success': False, 'message': 'Username is required!'}), 400

#     response = delete_user(username)
#     return jsonify(response), 400 if not response['success'] else 200

# if __name__ == '__main__':
#     app.run(debug=False, host='0.0.0.0', port=5000)