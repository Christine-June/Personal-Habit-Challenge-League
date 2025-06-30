from flask_restful import Resource
from flask import request, jsonify
from models import Challenge, ChallengeParticipant, ChallengeEntry, User, db
from schemas import ChallengeSchema
from datetime import datetime

challenge_schema = ChallengeSchema()
challenges_schema = ChallengeSchema(many=True)

class ChallengeListResource(Resource):
    def get(self):  # GET /challenges
        challenges = Challenge.query.all()
        return challenges_schema.dump(challenges), 200

    def post(self):  # POST /challenges
        data = request.get_json()
        required_fields = ["name", "description", "created_by", "start_date", "end_date"]
        for field in required_fields:
            if not data.get(field):
                return {"error": f"{field} is required"}, 400

        try:
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        except Exception:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400

        if start_date > end_date:
            return {"error": "Start date must be before or equal to end date"}, 400

        new_challenge = Challenge(
            name=data["name"],
            description=data["description"],
            created_by=data["created_by"],
            start_date=start_date,
            end_date=end_date,
        )

        db.session.add(new_challenge)
        db.session.commit()
        return challenge_schema.dump(new_challenge), 201

class ChallengeResource(Resource):
    def get(self, id):  # GET /challenges/<id>
        challenge = Challenge.query.get_or_404(id)
        return challenge_schema.dump(challenge), 200

    def patch(self, id):  # PATCH /challenges/<id>
        challenge = Challenge.query.get_or_404(id)
        data = request.get_json()

        if "start_date" in data or "end_date" in data:
            try:
                if "start_date" in data:
                    challenge.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
                if "end_date" in data:
                    challenge.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            except Exception:
                return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400

            if challenge.start_date > challenge.end_date:
                return {"error": "Start date must be before or equal to end date"}, 400

        if "name" in data:
            challenge.name = data["name"]
        if "description" in data:
            challenge.description = data["description"]
        if "created_by" in data:
            challenge.created_by = data["created_by"]

        db.session.commit()
        return challenge_schema.dump(challenge), 200

    def delete(self, id):  # DELETE /challenges/<id>
        challenge = Challenge.query.get_or_404(id)
        db.session.delete(challenge)
        db.session.commit()
        return {"message": "Challenge deleted"}, 200

# New: GET /challenges/<id>/participants
class ChallengeParticipantsResource(Resource):
    def get(self, id):
        challenge = Challenge.query.get_or_404(id)
        participants = [cp.user for cp in challenge.participants]
        return [p.to_dict() for p in participants], 200

    def post(self, id):
        data = request.get_json()
        username = data.get("username")

        challenge = Challenge.query.get_or_404(id)
        user = User.query.filter_by(username=username).first()

        if not user:
            return {"error": "User not found"}, 404

        existing = ChallengeParticipant.query.filter_by(user_id=user.id, challenge_id=id).first()
        if existing:
            return {"message": "User already joined"}, 200

        new_participant = ChallengeParticipant(user_id=user.id, challenge_id=id)
        db.session.add(new_participant)
        db.session.commit()
        return user.to_dict(), 201

# New: GET /challenges/<id>/entries
class ChallengeEntriesResource(Resource):
    def get(self, id):
        challenge = Challenge.query.get_or_404(id)
        entries = challenge.entries
        return [
            {
                "id": e.id,
                "username": e.user.username,
                "content": e.progress,
                "createdAt": e.date.isoformat(),
            }
            for e in entries
        ], 200
