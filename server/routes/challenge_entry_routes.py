from flask import Blueprint, jsonify

challenge_entry_bp = Blueprint('challenge_entry_bp', __name__)

@challenge_entry_bp.route('/', methods=['GET'])
def get_challenge_entries():
    return jsonify({"message": "All Challenge Entries Route Working!"})
