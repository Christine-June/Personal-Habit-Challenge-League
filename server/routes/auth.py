from flask import Flask, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from schemas import user_schema
from flask_bcrypt import generate_password_hash
from config import db

def register_auth_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON body"}, 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"error": "Username and password are required"}, 400

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token, "user": user_schema.dump(user)}, 200
        return {"error": "Invalid credentials"}, 401

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user_schema.dump(user), 200

    @app.route('/signup', methods=['POST', 'OPTIONS'])
    def signup():
        if request.method == 'OPTIONS':
            return {}, 200  # Allow preflight

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        avatar_url = data.get('avatar_url')  # <-- get avatar_url from request

        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 409
        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 409

        hashed_password = generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            avatar_url=avatar_url  # <-- save avatar_url
        )
        db.session.add(new_user)
        db.session.commit()
        return {"success": True, "user": user_schema.dump(new_user)}, 201