from flask import request, session
from flask_restful import Resource
from models import db, ChallengeEntry
from datetime import date

class ChallengeEntryList(Resource):
    def post(self):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        challenge_id = data.get("challenge_id")
        progress = data.get("progress")

        if not challenge_id or not progress:
            return {"error": "Challenge ID and progress are required"}, 400

        entry = ChallengeEntry(
            user_id=session["user_id"],
            challenge_id=challenge_id,
            progress=progress,
            date=date.today()
        )
        db.session.add(entry)
        db.session.commit()

        return {
            "message": "Challenge entry submitted",
            "entry": {
                "id": entry.id,
                "user_id": entry.user_id,
                "challenge_id": entry.challenge_id,
                "progress": entry.progress,
                "date": str(entry.date)
            }
        }, 201

    def get(self):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401

        entries = ChallengeEntry.query.filter_by(user_id=session["user_id"]).all()
        return [
            {
                "id": e.id,
                "challenge_id": e.challenge_id,
                "progress": e.progress,
                "date": str(e.date)
            } for e in entries
        ], 200
