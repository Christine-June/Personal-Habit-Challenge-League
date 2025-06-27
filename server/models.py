from datetime import datetime, date
from config import db
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

### --- User Model --- ###
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))

    # Relationships
    habits = db.relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    user_habits = db.relationship("UserHabit", back_populates="user", cascade="all, delete-orphan")
    habit_entries = db.relationship("HabitEntry", back_populates="user", cascade="all, delete-orphan")
    challenges_created = db.relationship("Challenge", back_populates="creator", cascade="all, delete-orphan")
    challenge_participations = db.relationship("ChallengeParticipant", back_populates="user", cascade="all, delete-orphan")
    challenge_entries = db.relationship("ChallengeEntry", back_populates="user", cascade="all, delete-orphan")
    sent_messages = db.relationship("Message", back_populates="sender", foreign_keys="Message.sender_id", cascade="all, delete-orphan")
    received_messages = db.relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")



    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


### --- Habit Model --- ###
class Habit(db.Model, SerializerMixin):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="habits")
    user_habits = db.relationship("UserHabit", back_populates="habit", cascade="all, delete-orphan")
    habit_entries = db.relationship("HabitEntry", back_populates="habit", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="habit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Habit {self.name}>"


### --- UserHabit Model --- ###
class UserHabit(db.Model, SerializerMixin):
    __tablename__ = "user_habits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date)

    # Relationships
    user = db.relationship("User", back_populates="user_habits")
    habit = db.relationship("Habit", back_populates="user_habits")

    __table_args__ = (
        db.UniqueConstraint("user_id", "habit_id", name="unique_user_habit"),
    )

    def __repr__(self):
        return f"<UserHabit user_id={self.user_id} habit_id={self.habit_id}>"


### --- HabitEntry Model --- ###
class HabitEntry(db.Model, SerializerMixin):
    __tablename__ = "habit_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    progress = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.String(255))  # optional notes field
    date = db.Column(db.Date, default=date.today)

    # Relationships
    user = db.relationship("User", back_populates="habit_entries")
    habit = db.relationship("Habit", back_populates="habit_entries")

    __table_args__ = (
        db.UniqueConstraint("user_id", "habit_id", "date", name="unique_habit_entry_per_day"),
    )

    @staticmethod
    def validate_progress(value):
        return value in ['completed', 'skipped', 'partial']

    def __repr__(self):
        return f"<HabitEntry user_id={self.user_id} habit_id={self.habit_id} date={self.date}>"


### --- Challenge Model --- ###
class Challenge(db.Model, SerializerMixin):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    creator = db.relationship("User", back_populates="challenges_created")
    participants = db.relationship("ChallengeParticipant", back_populates="challenge", cascade="all, delete-orphan")
    entries = db.relationship("ChallengeEntry", back_populates="challenge", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="challenge", cascade="all, delete-orphan")

    __table_args__ = (
        db.CheckConstraint("start_date < end_date", name="check_start_date_before_end_date"),
    )

    def __repr__(self):
        return f"<Challenge {self.name}>"


### --- ChallengeParticipant Model --- ###
class ChallengeParticipant(db.Model, SerializerMixin):
    __tablename__ = "challenge_participants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    joined_date = db.Column(db.Date, default=date.today)
    reason = db.Column(db.String(255))

    # Relationships
    user = db.relationship("User", back_populates="challenge_participations")
    challenge = db.relationship("Challenge", back_populates="participants")

    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", name="unique_user_challenge"),
    )

    def __repr__(self):
        return f"<ChallengeParticipant user_id={self.user_id} challenge_id={self.challenge_id}>"


### --- ChallengeEntry Model --- ###
class ChallengeEntry(db.Model, SerializerMixin):
    __tablename__ = "challenge_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    progress = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today)

    # Relationships
    user = db.relationship("User", back_populates="challenge_entries")
    challenge = db.relationship("Challenge", back_populates="entries")

    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", "date", name="unique_challenge_entry_per_day"),
    )

    def __repr__(self):
        return f"<ChallengeEntry user_id={self.user_id} challenge_id={self.challenge_id} date={self.date}>"


### --- Message Model --- ###
class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    reply_to_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    parent = db.relationship("Message", remote_side=[id], back_populates="replies", foreign_keys=[reply_to_id])
    replies = db.relationship("Message", back_populates="parent", cascade="all, delete-orphan", single_parent=True)

    serialize_rules = ("-sender.sent_messages", "-receiver.received_messages", "-replies.parent",)

    def __repr__(self):
        return f"<Message id={self.id} sender_id={self.sender_id} receiver_id={self.receiver_id}>"

### --- Comment Model --- ###
class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    user = db.relationship('User', back_populates='comments')
    habit = db.relationship('Habit', back_populates='comments', foreign_keys=[habit_id])
    challenge = db.relationship('Challenge', back_populates='comments', foreign_keys=[challenge_id])

    def __repr__(self):
        return f"<Comment id={self.id} user_id={self.user_id}>"



