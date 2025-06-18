from flask import Blueprint, jsonify

user_habit_bp = Blueprint('user_habit_bp', __name__)

@user_habit_bp.route('/', methods=['GET'])
def get_user_habits():
    return jsonify({"message": "All User-Habits Route Working!"})
