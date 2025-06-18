from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()


from routes.user_routes import user_bp
from routes.habit_routes import habit_bp
from routes.challenge_routes import challenge_bp
from routes.user_habit_routes import user_habit_bp
from routes.challenge_participant_routes import challenge_participant_bp
from routes.challenge_entry_routes import challenge_entry_bp
from routes.habit_entry_routes import habit_entry_bp

def create_app():
    app = Flask(__name__)

    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)
    migrate.init_app(app, db)

    
    CORS(app)

    
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(habit_bp, url_prefix='/habits')
    app.register_blueprint(challenge_bp, url_prefix='/challenges')
    app.register_blueprint(user_habit_bp, url_prefix='/user_habits')
    app.register_blueprint(challenge_participant_bp, url_prefix='/challenge_participants')
    app.register_blueprint(challenge_entry_bp, url_prefix='/challenge_entries')
    app.register_blueprint(habit_entry_bp, url_prefix='/habit_entries')

    return app
