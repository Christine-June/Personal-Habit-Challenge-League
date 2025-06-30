from flask_restful import Resource
from flask import request
from models import CalendarEntry
from config import db

class CalendarEntriesResource(Resource):
    def get(self):
        user_id = request.args.get("user_id", type=int)
        if not user_id:
            return {"error": "user_id is required"}, 400

        entries = CalendarEntry.query.filter_by(user_id=user_id).all()
        result = []
        for entry in entries:
            result.append({
                "id": entry.id,
                "type": entry.type,
                "name": entry.name,
                "description": entry.description,
                "progress": entry.progress,
                "notes": entry.notes,
                "date": entry.date.isoformat(),
                "time": entry.time,
            })
        return {"entries": result}, 200