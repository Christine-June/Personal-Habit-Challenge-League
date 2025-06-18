from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
class ChallengeEntry(db.Model):
    __tablename__ = "challenge_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    progress = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today)

    user = db.relationship("User", back_populates="challenge_entries")
    challenge = db.relationship("Challenge", back_populates="entries")

    __table_args__ = (
        db.UniqueConstraint("user_id", "challenge_id", "date", name="unique_challenge_entry_per_day"),
    )