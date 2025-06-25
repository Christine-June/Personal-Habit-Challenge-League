from flask import request, session, Blueprint
from flask_restful import Resource
from models import db, ChallengeEntry, ChallengeParticipant, Challenge
from datetime import date


class ChallengeEntryRoutes(Resource):
    def get(self):
        """View all your submitted entries"""
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        entries = ChallengeEntry.query.filter_by(user_id=user_id).order_by(ChallengeEntry.date.desc()).all()

        return [
            {
                "id": e.id,
                "challenge_id": e.challenge_id,
                "progress": e.progress,
                "date": str(e.date)
            } for e in entries
        ], 200

    def post(self):
        """Submit a new activity entry for a challenge"""
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        challenge_id = data.get("challenge_id")
        progress = data.get("progress")

        if not challenge_id or not progress:
            return {"error": "Challenge ID and progress are required"}, 400

        # Check challenge exists
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return {"error": "Challenge not found"}, 404

        # Check challenge is active
        if getattr(challenge, "status", "active") != "active":
            return {"error": "Challenge is not currently active"}, 403

        # Check user is a participant
        is_participant = ChallengeParticipant.query.filter_by(
            user_id=user_id,
            challenge_id=challenge_id
        ).first()
        if not is_participant:
            return {"error": "You must join this challenge before submitting"}, 403

        # Prevent duplicate entry per day
        today = date.today()
        existing_entry = ChallengeEntry.query.filter_by(
            user_id=user_id,
            challenge_id=challenge_id,
            date=today
        ).first()
        if existing_entry:
            return {"error": "You already submitted an entry for today"}, 409

        # Create new entry
        entry = ChallengeEntry(
            user_id=user_id,
            challenge_id=challenge_id,
            progress=progress,
            date=today
        )

        db.session.add(entry)
        db.session.commit()

        return {
            "message": "Entry submitted",
            "entry": {
                "id": entry.id,
                "challenge_id": entry.challenge_id,
                "progress": entry.progress,
                "date": str(entry.date)
            }
        }, 201


