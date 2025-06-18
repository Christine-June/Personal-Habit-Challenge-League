from flask import request, session, jsonify
from flask_restful import Resource
from models import db, ChallengeParticipant
from datetime import date

class ChallengeParticipantList(Resource):
    def post(self):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        challenge_id = data.get("challenge_id")

        if not challenge_id:
            return {"error": "Challenge ID is required"}, 400

        # Check for duplicate participation
        existing = ChallengeParticipant.query.filter_by(
            user_id=session["user_id"], challenge_id=challenge_id
        ).first()

        if existing:
            return {"error": "Already joined this challenge"}, 400

        participant = ChallengeParticipant(
            user_id=session["user_id"],
            challenge_id=challenge_id,
            joined_date=date.today()
        )
        db.session.add(participant)
        db.session.commit()

        return {
            "message": "Joined challenge successfully",
            "participant": {
                "id": participant.id,
                "user_id": participant.user_id,
                "challenge_id": participant.challenge_id,
                "joined_date": str(participant.joined_date)
            }
        }, 201
