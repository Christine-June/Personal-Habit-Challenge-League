from flask_restful import Resource
from flask import session
from models import User, Habit, Challenge, Comment, ChallengeParticipant

class FeedResource(Resource):
    def get(self):
        user_id = session.get("user_id")
        habits = Habit.query.order_by(Habit.id.desc()).limit(10).all()
        challenges = Challenge.query.order_by(Challenge.id.desc()).limit(10).all()

        feed_items = []

        for h in habits:
            feed_items.append({
                "type": "habit",
                "id": h.id,
                "title": h.name,
                "description": h.description,
                "user": User.query.get(h.user_id).username if h.user_id else "Unknown",
                "comments": [
                    {
                        "id": c.id,
                        "content": c.content,
                        "user": User.query.get(c.user_id).username if c.user_id else "Unknown"
                    }
                    for c in Comment.query.filter_by(habit_id=h.id).all()
                ]
            })

        for c in challenges:
            joined = False
            if user_id:
                joined = ChallengeParticipant.query.filter_by(
                    user_id=user_id, challenge_id=c.id
                ).first() is not None
            feed_items.append({
                "type": "challenge",
                "id": c.id,
                "title": c.name,
                "description": c.description,
                "user": User.query.get(c.created_by).username if c.created_by else "Unknown",
                "created_by": c.created_by,
                "joined": joined,
                "comments": [
                    {
                        "id": cm.id,
                        "content": cm.content,
                        "user": User.query.get(cm.user_id).username if cm.user_id else "Unknown"
                    }
                    for cm in Comment.query.filter_by(challenge_id=c.id).all()
                ]
            })

        feed_items.sort(key=lambda x: x["id"], reverse=True)
        return feed_items, 200