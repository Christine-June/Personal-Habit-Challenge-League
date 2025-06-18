from flask import Blueprint, jsonify

challenge_bp = Blueprint('challenge_bp', __name__)

@challenge_bp.route('/', methods=['GET'])
def get_challenges():
    return jsonify({"message": "All Challenges Route Working!"})
