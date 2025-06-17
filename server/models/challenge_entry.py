from . import db
from datetime import date

class ChallengeEntry(db.Model):
    __tablename__ = 'challenge_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    progress = db.Column(db.String(255))  # e.g., note or score text
    status = db.Column(db.String(50), nullable=False)  # e.g., 'in_progress', 'completed', 'failed'
    