from flask import Flask
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
from routes.user_routes import UserListResource, UserResource
from routes.user_habit_routes import UserHabitsResource, AssignHabitResource, RemoveHabitResource
from routes.message_routes import MessageListResource
from routes.challenge_routes import ChallengeListResource, ChallengeResource
from routes.habit_entry_routes import HabitEntryListResource, HabitEntryResource
from routes.challenge_entry_routes import ChallengeEntryRoutes
from routes.challenge_participant_routes import ChallengeParticipantRoutes, ParticipationStatus
from routes.auth import register_auth_routes

load_dotenv()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # <-- This enables CORS for all routes
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
    api.add_resource(UserHabitsResource, '/user-habits/<int:user_id>')
    api.add_resource(AssignHabitResource, '/user-habits/assign')
    api.add_resource(RemoveHabitResource, '/user-habits/remove')
    api.add_resource(MessageListResource, '/messages')
    api.add_resource(ChallengeListResource, '/challenges', '/challenges/')
    api.add_resource(ChallengeResource, '/challenges/<int:id>')
    api.add_resource(HabitEntryListResource, '/habit-entries', '/habit-entries/')
    api.add_resource(HabitEntryResource, '/habit-entries/<int:entry_id>')
    api.add_resource(ChallengeEntryRoutes, '/challenge-entries')
    api.add_resource(ChallengeParticipantRoutes, '/challenge-participants')
    api.add_resource(ParticipationStatus, '/challenges/<int:challenge_id>/participation-status')

    register_auth_routes(app)

    @app.route("/")
    def index():
        return {"message": "Welcome to the API!"}, 200

    return app

app = create_app()