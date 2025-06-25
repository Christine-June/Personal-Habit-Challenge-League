from flask_restful import Resource
from flask import request
from models import db, User, Habit
from schemas import HabitSchema

habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)

class UserHabitsResource(Resource):
    def get(self, user_id):  # GET /user-habits/<user_id>
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        habits = user.habits
        return {"user_id": user_id, "habits": habits_schema.dump(habits)}, 200

class AssignHabitResource(Resource):
    def post(self):  # POST /user-habits/assign
        data = request.get_json()
        user_id = data.get('user_id')
        habit_id = data.get('habit_id')
        if not user_id or not habit_id:
            return {"error": "user_id and habit_id are required"}, 400

        user = User.query.get(user_id)
        habit = Habit.query.get(habit_id)
        if not user or not habit:
            return {"error": "User or Habit not found"}, 404

        if habit in user.habits:
            return {"message": "Habit already assigned to user"}, 200

        user.habits.append(habit)
        db.session.commit()
        return {"message": f"Habit {habit_id} assigned to user {user_id}"}, 201

class RemoveHabitResource(Resource):
    def delete(self):  # DELETE /user-habits/remove
        data = request.get_json()
        user_id = data.get('user_id')
        habit_id = data.get('habit_id')
        if not user_id or not habit_id:
            return {"error": "user_id and habit_id are required"}, 400

        user = User.query.get(user_id)
        habit = Habit.query.get(habit_id)
        if not user or not habit:
            return {"error": "User or Habit not found"}, 404

        if habit not in user.habits:
            return {"message": "Habit not assigned to user"}, 200

        user.habits.remove(habit)
        db.session.commit()
        return {"message": f"Habit {habit_id} removed from user {user_id}"}, 200
