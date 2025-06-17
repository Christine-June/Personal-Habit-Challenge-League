from . import db
from datetime import date

class ChallengeParticipant(db.Model):
    __tablename__ = 'challenge_participants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    joined_date = db.Column(db.Date, default=date.today)
    left_date = db.Column(db.Date, nullable=True)  # Nullable if the user is still participating
    status = db.Column(db.String(50), nullable=False)  # e.g., 'active', 'completed', 'withdrawn'