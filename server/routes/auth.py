from flask import Flask, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from schemas import user_schema  # Make sure user_schema is defined in your schemas.py

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