from datetime import datetime, date
from config import db
from werkzeug.security import generate_password_hash, check_password_hash  # 🔑 Import for password hashing

### --- User Model --- ###
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)  # ✅ Added avatar field

    # Relationships
    habits = db.relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    user_habits = db.relationship("UserHabit", back_populates="user", cascade="all, delete-orphan")
    habit_entries = db.relationship("HabitEntry", back_populates="user", cascade="all, delete-orphan")
    challenges_created = db.relationship("Challenge", back_populates="creator", cascade="all, delete-orphan")
    challenge_participations = db.relationship("ChallengeParticipant", back_populates="user", cascade="all, delete-orphan")
    challenge_entries = db.relationship("ChallengeEntry", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatarUrl": self.avatar_url or "/placeholder-avatar.svg"  # Default avatar fallback
        }

    # ✅ Password hashing methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

### --- Habit Model --- ###
class Habit(db.Model):
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

    def __repr__(self):
        return f"<Habit {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "user_id": self.user_id,
        }


### --- UserHabit Model --- ###
class UserHabit(db.Model):
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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "habit_id": self.habit_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }


### --- HabitEntry Model --- ###
class HabitEntry(db.Model):
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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "habit_id": self.habit_id,
            "progress": self.progress,
            "notes": self.notes,
            "date": self.date.isoformat() if self.date else None,
        }


### --- Challenge Model --- ###
class Challenge(db.Model):
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

    __table_args__ = (
        db.CheckConstraint("start_date < end_date", name="check_start_date_before_end_date"),
    )

    def __repr__(self):
        return f"<Challenge {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


### --- ChallengeParticipant Model --- ###
class ChallengeParticipant(db.Model):
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

    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", "date", name="unique_challenge_entry_per_day"),
    )

    def __repr__(self):
        return f"<ChallengeEntry user_id={self.user_id} challenge_id={self.challenge_id} date={self.date}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "challenge_id": self.challenge_id,
            "progress": self.progress,
            "date": self.date.isoformat() if self.date else None,
        }
