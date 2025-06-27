from flask import session, jsonify, request
from flask_restful import Resource
from models import User, db, Habit, Challenge, ChallengeParticipant
from schemas import UserSchema, user_schema, habits_schema, challenges_schema
from sqlalchemy import func

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users), 200

    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 409

        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 409

        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Use Flask-Bcrypt

        try:
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user), 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to register user: {e}"}, 500

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user_schema.dump(user), 200

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if email and email != user.email and User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 409

        if username and username != user.username and User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 409

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)  # Use Flask-Bcrypt

        try:
            db.session.commit()
            return user_schema.dump(user), 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update user: {e}"}, 500

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete user: {e}"}, 500

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return {"user": user_schema.dump(user)}, 200
        return {"error": "Invalid credentials"}, 401

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        bio = data.get("bio", "")
        avatar_url = data.get("avatar_url", "")

        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 409
        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 409

        user = User(username=username, email=email, bio=bio, avatar_url=avatar_url)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return {"user": user_schema.dump(user)}, 201

class UserProfileResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

class CurrentUserResource(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
