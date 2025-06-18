from sqlalchemy_serializer import SerializerMixin
from app import db


from datetime import datetime, date
from config import db

### --- User Model --- ###
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user_habits = db.relationship('UserHabit', back_populates='user', cascade='all, delete-orphan')
    challenges_created = db.relationship('Challenge', foreign_keys='Challenge.created_by', back_populates='creator', cascade='all, delete-orphan')
    challenge_participations = db.relationship('ChallengeParticipant', back_populates='user', cascade='all, delete-orphan')
    challenge_entries = db.relationship('ChallengeEntry', back_populates='user', cascade='all, delete-orphan')
    habit_entries = db.relationship('HabitEntry', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = (
        '-user_habits.user',
        '-challenges_created.creator',
        '-challenge_participations.user',
        '-challenge_entries.user',
        '-habit_entries.user',
        '-password_hash'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


### --- HabitEntry Model --- ###
class HabitEntry(db.Model, SerializerMixin):
    __tablename__ = 'habit_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='habit_entries')
    habit = db.relationship('Habit', back_populates='entries')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'habit_id', 'date', name='unique_habit_log_per_day'),
        db.CheckConstraint("status IN ('completed', 'skipped', 'partial')", name='valid_habit_status'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'habit_id': self.habit_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def validate_status(cls, status):
        return status.lower() in ['completed', 'skipped', 'partial']


### --- ChallengeParticipant Model --- ###
class ChallengeParticipant(db.Model):
    __tablename__ = "challenge_participants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    joined_date = db.Column(db.Date, default=date.today)
    reason = db.Column(db.String(255))  # Optional: motivation or goal for joining

    # Relationships
    user = db.relationship("User", back_populates="challenge_participations")
    challenge = db.relationship("Challenge", back_populates="participants")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", name="unique_user_challenge"),
    )

    def __repr__(self):
        return f"<ChallengeParticipant id={self.id} user_id={self.user_id} challenge_id={self.challenge_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "challenge_id": self.challenge_id,
            "joined_date": self.joined_date.isoformat() if self.joined_date else None,
            "reason": self.reason,
        }


### --- ChallengeEntry Model --- ###
class ChallengeEntry(db.Model):
    __tablename__ = "challenge_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    progress = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today)

    # Relationships
    user = db.relationship("User", back_populates="challenge_entries")
    challenge = db.relationship("Challenge", back_populates="entries")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", "date", name="unique_challenge_entry_per_day"),
    )

    def __repr__(self):
        return f"<ChallengeEntry id={self.id} user_id={self.user_id} challenge_id={self.challenge_id} date={self.date}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "challenge_id": self.challenge_id,
            "progress": self.progress,
            "date": self.date.isoformat() if self.date else None,
        }
