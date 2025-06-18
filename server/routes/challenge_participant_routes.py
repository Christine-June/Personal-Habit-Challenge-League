from flask import request, session
from flask_restful import Resource
from models import db, ChallengeParticipant, Challenge
from datetime import date


class ChallengeParticipantRoutes(Resource):
    def get(self):
        """View all challenges the user has joined"""
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        participations = ChallengeParticipant.query.filter_by(user_id=user_id).all()

        return [
            {
                "challenge_id": p.challenge.id,
                "name": p.challenge.name,
                "description": p.challenge.description,
                "start_date": str(p.challenge.start_date),
                "status": p.challenge.status,
                "joined_date": str(p.joined_date),
                "reason": p.reason
            }
            for p in participations
        ], 200

    def post(self):
        """Join a challenge"""
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        challenge_id = data.get("challenge_id")
        reason = data.get("reason", "")

        if not challenge_id:
            return {"error": "Missing challenge_id"}, 400

        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return {"error": "Challenge not found"}, 404

        # Prevent duplicate join
        already_joined = ChallengeParticipant.query.filter_by(
            user_id=user_id, challenge_id=challenge_id
        ).first()
        if already_joined:
            return {"error": "Already joined this challenge"}, 409

        # Prevent joining if challenge has started
        if challenge.start_date and challenge.start_date <= date.today():
            return {"error": "Challenge already started, can't join"}, 403

        # Limit concurrent active joins
        active_count = ChallengeParticipant.query.filter_by(user_id=user_id).count()
        if active_count >= 3:
            return {"error": "Limit reached: only 3 concurrent challenges allowed"}, 403

        # Create new participation
        participation = ChallengeParticipant(
            user_id=user_id,
            challenge_id=challenge_id,
            reason=reason,
            joined_date=date.today()
        )
        db.session.add(participation)
        db.session.commit()

        # Return current rank (e.g., 15th to join)
        rank = ChallengeParticipant.query.filter_by(challenge_id=challenge_id).count()

        return {
            "message": "Joined successfully",
            "rank": rank,
            "challenge_id": challenge_id
        }, 201

    def delete(self):
        """Leave a challenge"""
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        challenge_id = data.get("challenge_id")

        if not challenge_id:
            return {"error": "Missing challenge_id"}, 400

        participation = ChallengeParticipant.query.filter_by(
            user_id=user_id, challenge_id=challenge_id
        ).first()

        if not participation:
            return {"error": "Not a participant in this challenge"}, 404

        db.session.delete(participation)
        db.session.commit()

        return {"message": "Left the challenge successfully"}, 200


class ParticipationStatus(Resource):
    def get(self, challenge_id):
        """Check if the user has joined a specific challenge"""
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        joined = ChallengeParticipant.query.filter_by(
            user_id=user_id, challenge_id=challenge_id
        ).first() is not None

        return {"joined": joined}, 200
