from flask import Blueprint, request, jsonify
from models import Habit, db

habit_bp = Blueprint('habit_bp', __name__, url_prefix='/habits')

@habit_bp.route('/', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([habit.to_dict() for habit in habits])

@habit_bp.route('/<int:id>', methods=['GET'])
def get_habit(id):
    habit = Habit.query.get_or_404(id)
    return jsonify(habit.to_dict())

@habit_bp.route('/', methods=['POST'])
def create_habit():
    data = request.get_json()
    new_habit = Habit(
        name=data.get('name'),
        description=data.get('description')
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify(new_habit.to_dict()), 201

@habit_bp.route('/<int:id>', methods=['PATCH'])
def update_habit(id):
    habit = Habit.query.get_or_404(id)
    data = request.get_json()
    habit.name = data.get('name', habit.name)
    habit.description = data.get('description', habit.description)
    db.session.commit()
    return jsonify(habit.to_dict())

@habit_bp.route('/<int:id>', methods=['DELETE'])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted"})
