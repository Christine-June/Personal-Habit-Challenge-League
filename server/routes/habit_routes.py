from flask_restful import Resource
from flask import request
from models import db, Habit
from schemas import HabitSchema

habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)

class HabitListResource(Resource):
    def get(self):  # GET /habits
        habits = Habit.query.all()
        return habits_schema.dump(habits), 200

    def post(self):  # POST /habits
        data = request.get_json()
        # Validation
        required_fields = ["name", "user_id"]
        for field in required_fields:
            if not data.get(field):
                return {"error": f"{field} is required"}, 400

        if "frequency" in data and data["frequency"] not in ["daily", "weekly", "monthly"]:
            return {"error": "Frequency must be daily, weekly, or monthly"}, 400

        new_habit = Habit(
            name=data["name"],
            description=data.get("description"),
            frequency=data.get("frequency"),
            user_id=data["user_id"]
        )
        db.session.add(new_habit)
        db.session.commit()
        return habit_schema.dump(new_habit), 201

class HabitResource(Resource):
    def get(self, habit_id):  # GET /habits/<id>
        habit = Habit.query.get(habit_id)
        if habit:
            return habit_schema.dump(habit), 200
        return {"error": "Habit not found"}, 404

    def patch(self, habit_id):  # PATCH /habits/<id>
        habit = Habit.query.get(habit_id)
        if not habit:
            return {"error": "Habit not found"}, 404
        data = request.get_json()
        if "frequency" in data and data["frequency"] not in ["daily", "weekly", "monthly"]:
            return {"error": "Frequency must be daily, weekly, or monthly"}, 400
        habit.name = data.get('name', habit.name)
        habit.description = data.get('description', habit.description)
        habit.frequency = data.get('frequency', habit.frequency)
        db.session.commit()
        return habit_schema.dump(habit), 200

    def delete(self, habit_id):  # DELETE /habits/<id>
        habit = Habit.query.get(habit_id)
        if not habit:
            return {"error": "Habit not found"}, 404
        db.session.delete(habit)
        db.session.commit()
        return {"message": "Habit deleted"}, 200
