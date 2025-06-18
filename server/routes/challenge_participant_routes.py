from flask import Blueprint, jsonify

challenge_participant_bp = Blueprint('challenge_participant_bp', __name__)

@challenge_participant_bp.route('/', methods=['GET'])
def get_challenge_participants():
    return jsonify({"message": "All Challenge Participants Route Working!"})
