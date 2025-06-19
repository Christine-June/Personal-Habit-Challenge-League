from flask import Blueprint, request, jsonify
from models import db, User, Habit, UserHabit

user_habit_bp = Blueprint('user_habit_bp', __name__)

@user_habit_bp.route('/<int:user_id>', methods=['GET'])
def get_user_habits(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    habits = [habit.to_dict() for habit in user.habits]
    return jsonify({"user_id": user_id, "habits": habits})

@user_habit_bp.route('/assign', methods=['POST'])
def assign_habit_to_user():
    data = request.get_json()
    user_id = data.get('user_id')
    habit_id = data.get('habit_id')
    if not user_id or not habit_id:
        return jsonify({"error": "user_id and habit_id are required"}), 400

    user = User.query.get(user_id)
    habit = Habit.query.get(habit_id)
    if not user or not habit:
        return jsonify({"error": "User or Habit not found"}), 404

    if habit in user.habits:
        return jsonify({"message": "Habit already assigned to user"}), 200

    user.habits.append(habit)
    db.session.commit()
    return jsonify({"message": f"Habit {habit_id} assigned to user {user_id}"}), 201

@user_habit_bp.route('/remove', methods=['DELETE'])
def remove_habit_from_user():
    data = request.get_json()
    user_id = data.get('user_id')
    habit_id = data.get('habit_id')
    if not user_id or not habit_id:
        return jsonify({"error": "user_id and habit_id are required"}), 400

    user = User.query.get(user_id)
    habit = Habit.query.get(habit_id)
    if not user or not habit:
        return jsonify({"error": "User or Habit not found"}), 404

    if habit not in user.habits:
        return jsonify({"message": "Habit not assigned to user"}), 200

    user.habits.remove(habit)
    db.session.commit()
    return jsonify({"message": f"Habit {habit_id} removed from user {user_id}"}), 200
