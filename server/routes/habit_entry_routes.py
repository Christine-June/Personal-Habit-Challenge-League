from flask import Blueprint, jsonify

habit_entry_bp = Blueprint('habit_entry_bp', __name__)

@habit_entry_bp.route('/', methods=['GET'])
def get_habit_entries():
    return jsonify({"message": "All Habit Entries Route Working!"})
