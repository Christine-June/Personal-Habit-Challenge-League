from flask import Blueprint, request, jsonify
from models import db, Habit, User
from datetime import date

habits_bp = Blueprint('habits_bp', __name__, url_prefix='/habits')

# Get all habits
@habits_bp.route('/', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([habit.to_dict() for habit in habits]), 200

# Get a single habit by ID
@habits_bp.route('/<int:habit_id>', methods=['GET'])
def get_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        return jsonify(habit.to_dict()), 200
    return jsonify({"error": "Habit not found"}), 404

# Create a new habit
@habits_bp.route('/', methods=['POST'])
def create_habit():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    user_id = data.get('user_id')

    if not name or not user_id:
        return jsonify({"error": "Name and user_id are required"}), 400

    habit = Habit(name=name, description=description, user_id=user_id)
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit.to_dict()), 201

# Update a habit
@habits_bp.route('/<int:habit_id>', methods=['PATCH'])
def update_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    data = request.get_json()
    habit.name = data.get('name', habit.name)
    habit.description = data.get('description', habit.description)
    db.session.commit()
    return jsonify(habit.to_dict()), 200

# Delete a habit
@habits_bp.route('/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted"}), 200
