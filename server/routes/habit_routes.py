from flask import Blueprint, jsonify

habit_bp = Blueprint('habit_bp', __name__)

@habit_bp.route('/', methods=['GET'])
def get_habits():
    return jsonify({"message": "All Habits Route Working!"})
