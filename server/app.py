from flask import Flask, request, jsonify
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

    # ✅ Full CORS config to prevent preflight errors
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # ✅ Allow handling of OPTIONS requests manually
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 200

    # ✅ Register blueprints
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

    # ✅ Signup route
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201

    # ✅ Login route
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    return app


app = create_app()