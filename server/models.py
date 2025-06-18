from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

from config import db

# Models go here!

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships based on the diagram
    user_habits = db.relationship('UserHabit', back_populates='user', cascade='all, delete-orphan')
    challenges_created = db.relationship('Challenge', foreign_keys='Challenge.created_by', back_populates='creator', cascade='all, delete-orphan')
    challenge_participants = db.relationship('ChallengeParticipant', back_populates='user', cascade='all, delete-orphan')
    challenge_entries = db.relationship('ChallengeEntry', back_populates='user', cascade='all, delete-orphan')
    habit_entries = db.relationship('HabitEntry', back_populates='user', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = (
        '-user_habits.user',
        '-challenges_created.creator',
        '-challenge_participants.user',
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
    
    def __repr__(self):
        return f'<User {self.username}>'

class Habit(db.Model, SerializerMixin):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_habits = db.relationship('UserHabit', back_populates='habit', cascade='all, delete-orphan')
    habit_entries = db.relationship('HabitEntry', back_populates='habit', cascade='all, delete-orphan')
    
    serialize_rules = ('-user_habits.habit', '-habit_entries.habit')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Habit {self.name}>'


class HabitEntry(db.Model, SerializerMixin):
    __tablename__ = 'habit_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    status = db.Column(db.String(50), nullable=False)  # 'completed', 'skipped', 'partial'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='habit_entries')
    habit = db.relationship('Habit', back_populates='entries')
    
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
        valid_statuses = ['completed', 'skipped', 'partial']
        return status.lower() in valid_statuses
