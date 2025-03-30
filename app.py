from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# In-memory user storage
users = []
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    # For now, just add to dummy users list (you can use DB later)
    for user in users:
        if user['email'] == email:
            return jsonify({"message": "Email already registered"}), 400

    users.append({
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "username": email.split('@')[0],  # Optional: auto username
        "password": password
    })

    return jsonify({"message": "Registration successful!"}), 200

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate fields
    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    # Find user
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
