from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Models (import or define here for demo) ---
# You can import your models if they're in a package:
# from server.models.challenge_entry import ChallengeEntry
#from server.models.chalenge_participant import ChallengeParticipant

class ChallengeEntry(db.Model):
    __tablename__ = 'challenge_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    progress = db.Column(db.String(255))
    status = db.Column(db.String(50), nullable=False)

class ChallengeParticipant(db.Model):
    __tablename__ = 'challenge_participants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    joined_date = db.Column(db.Date, default=date.today)
    left_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # Add other fields as needed

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    # Add other fields as needed

# --- Routes ---

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Personal Habit Challenge League API!"})

@app.route('/challenge_entries', methods=['GET'])
def get_challenge_entries():
    entries = ChallengeEntry.query.all()
    return jsonify([
        {
            "id": e.id,
            "user_id": e.user_id,
            "challenge_id": e.challenge_id,
            "date": e.date.isoformat(),
            "progress": e.progress,
            "status": e.status
        } for e in entries
    ])

@app.route('/challenge_participants', methods=['GET'])
def get_challenge_participants():
    participants = ChallengeParticipant.query.all()
    return jsonify([
        {
            "id": p.id,
            "user_id": p.user_id,
            "challenge_id": p.challenge_id,
            "joined_date": p.joined_date.isoformat(),
            "left_date": p.left_date.isoformat() if p.left_date else None,
            "status": p.status
        } for p in participants
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)