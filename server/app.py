from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

from config import db
from models import (
    User,
    Habit,
    UserHabit,
    Challenge,
    HabitEntry,
    ChallengeEntry,
    ChallengeParticipant,
)

# Import your blueprints
from routes.user_routes import user_bp
from routes.habit_routes import habits_bp
from routes.habit_entry_routes import habit_entry_bp
from routes.challenge_routes import challenge_bp
from routes.challenge_entry_routes import challenge_entry_bp
from routes.challenge_participant_routes import challenge_participant_bp
from routes.user_habit_routes import user_habit_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(habit_entry_bp)
    app.register_blueprint(challenge_bp)
    app.register_blueprint(challenge_entry_bp)
    app.register_blueprint(challenge_participant_bp)
    app.register_blueprint(user_habit_bp)

    @app.route("/")
    def index():
        return {"message": "Welcome to the API!"}, 200

    return app


app = create_app()