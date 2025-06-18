from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ==========================
# User Model
# ==========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)

    challenge_participants = db.relationship("ChallengeParticipant", backref="user", cascade="all, delete-orphan")
    challenge_entries = db.relationship("ChallengeEntry", backref="user", cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

# ==========================
# Challenge Model
# ==========================
class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    participants = db.relationship("ChallengeParticipant", backref="challenge", cascade="all, delete-orphan")
    entries = db.relationship("ChallengeEntry", backref="challenge", cascade="all, delete-orphan")

class ChallengeParticipant(db.Model):
    __tablename__ = "challenge_participants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    joined_date = db.Column(db.Date, default=date.today)

    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", name="unique_participation"),
    )

class ChallengeEntry(db.Model):
    __tablename__ = "challenge_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    progress = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today)

    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", "date", name="unique_entry_per_day"),
    )
