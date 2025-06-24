from flask import Flask, request, jsonify
from models import User  # Assuming you have a User model in models.py

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Instead of just returning a message, also return user data
        return jsonify({
            "message": "Login succeeded",
            "user": user.to_dict()  # Make sure to_dict() returns user info
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ...existing code...