from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash
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

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)

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
            user.password_hash = generate_password_hash(password)

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

class UserProfileResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        # Habits created by user
        habits = Habit.query.filter_by(user_id=user_id).all()
        # Challenges user is participating in
        challenge_part_ids = [cp.challenge_id for cp in ChallengeParticipant.query.filter_by(user_id=user_id).all()]
        challenges = Challenge.query.filter(Challenge.id.in_(challenge_part_ids)).all()

        # Calculate stats
        streak = 0  # You can implement streak logic if you want
        stats = {
            "habits": len(habits),
            "challenges": len(challenges),
            "streak": streak,
        }

        return {
            "id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
            "bio": getattr(user, "bio", ""),
            "stats": stats,
            "habits": [
                {"id": h.id, "name": h.name, "description": h.description}
                for h in habits
            ],
            "challenges": [
                {"id": c.id, "name": c.name, "description": c.description}
                for c in challenges
            ],
        }, 200
