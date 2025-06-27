from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

from config import db
from models import (
    User,
    Habit,
    UserHabit,
    Challenge,
    HabitEntry,
    ChallengeEntry,
    ChallengeParticipant,
    Message,
)
from schemas import ma

from routes.habit_routes import HabitListResource, HabitResource
from routes.user_routes import UserListResource, UserResource, LoginResource, SignupResource, UserProfileResource
from routes.user_habit_routes import UserHabitsResource, AssignHabitResource, RemoveHabitResource
from routes.message_routes import MessageListResource
from routes.challenge_routes import ChallengeListResource, ChallengeResource
#from routes.habit_entry_routes import HabitEntryListResource, HabitEntryResource
from routes.challenge_entry_routes import ChallengeEntryRoutes
from routes.challenge_participant_routes import ChallengeParticipantRoutes, ParticipationStatus
from routes.auth import register_auth_routes
from routes.feed_routes import FeedResource
from routes.user_routes import CurrentUserResource

load_dotenv()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")  # <-- Add this line
    CORS(app, supports_credentials=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret")
    app.json.compact = False
    jwt = JWTManager(app)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    bcrypt.init_app(app)

    # Register all resources
    api.add_resource(HabitListResource, '/habits', '/habits/')
    api.add_resource(HabitResource, '/habits/<int:habit_id>')
    api.add_resource(UserListResource, '/users', '/users/')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(LoginResource, "/login")
    api.add_resource(SignupResource, "/signup")
    api.add_resource(UserProfileResource, "/users/<int:user_id>/profile")
    api.add_resource(UserHabitsResource, '/user-habits/<int:user_id>')
    api.add_resource(AssignHabitResource, '/user-habits/assign')
    api.add_resource(RemoveHabitResource, '/user-habits/remove')
    api.add_resource(MessageListResource, '/messages')
    api.add_resource(ChallengeListResource, '/challenges', '/challenges/')
    api.add_resource(ChallengeResource, '/challenges/<int:id>')
    #api.add_resource(HabitEntryListResource, '/habit-entries', '/habit-entries/')
    #api.add_resource(HabitEntryResource, '/habit-entries/<int:entry_id>')
    api.add_resource(ChallengeEntryRoutes, '/challenge-entries')
    api.add_resource(ChallengeParticipantRoutes, '/challenge-participants')
    api.add_resource(ParticipationStatus, '/challenges/<int:challenge_id>/participation-status')
    api.add_resource(FeedResource, '/feed')
    api.add_resource(CurrentUserResource, "/me")

    register_auth_routes(app)

    @app.route("/")
    def index():
        return {"message": "Welcome to the API!"}, 200

    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.json
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        # ... handle other fields ...
        db.session.commit()
        return jsonify({"success": True, "user": user.to_dict()})

    # Add CORS headers to all responses (including errors)
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        return response

    return app

app = create_app()