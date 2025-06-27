from flask import request, session
from flask_restful import Resource
from models import Challenge, db
from schemas import challenge_schema
from datetime import datetime

class ChallengeListResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        # Convert string to date object
        try:
            start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
            end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        except Exception:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400
        created_by = data.get("created_by") or session.get("user_id")

        if not all([name, description, start_date, end_date, created_by]):
            return {"error": "All fields are required"}, 400

        challenge = Challenge(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            created_by=created_by
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge_schema.dump(challenge), 201

class ChallengeResource(Resource):
    def get(self, id):
        challenge = Challenge.query.get(id)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        return challenge_schema.dump(challenge), 200

    def delete(self, id):
        challenge = Challenge.query.get(id)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        db.session.delete(challenge)
        db.session.commit()
        return {"message": "Challenge deleted"}, 200

    def patch(self, id):
        challenge = Challenge.query.get(id)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        data = request.get_json()
        challenge.name = data.get("name", challenge.name)
        challenge.description = data.get("description", challenge.description)
        challenge.start_date = data.get("start_date", challenge.start_date)
        challenge.end_date = data.get("end_date", challenge.end_date)
        db.session.commit()
        return challenge_schema.dump(challenge), 200
