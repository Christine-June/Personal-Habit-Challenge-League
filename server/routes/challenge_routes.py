from flask import Blueprint, request, jsonify
from models import Challenge, db


challenge_bp = Blueprint('challenge_bp', __name__, url_prefix='/challenges')

@challenge_bp.route('/', methods=['GET'])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([c.to_dict() for c in challenges])

@challenge_bp.route('/<int:id>', methods=['GET'])
def get_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    return jsonify(challenge.to_dict())

@challenge_bp.route('/', methods=['POST'])
def create_challenge():
    data = request.get_json()
    new_challenge = Challenge(
        name=data.get('name'),
        description=data.get('description'),
        created_by=data.get('created_by')
    )
    db.session.add(new_challenge)
    db.session.commit()
    return jsonify(new_challenge.to_dict()), 201

@challenge_bp.route('/<int:id>', methods=['PATCH'])
def update_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    data = request.get_json()
    challenge.name = data.get('name', challenge.name)
    challenge.description = data.get('description', challenge.description)
    db.session.commit()
    return jsonify(challenge.to_dict())

@challenge_bp.route('/<int:id>', methods=['DELETE'])
def delete_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    db.session.delete(challenge)
    db.session.commit()
    return jsonify({"message": "Challenge deleted"})
