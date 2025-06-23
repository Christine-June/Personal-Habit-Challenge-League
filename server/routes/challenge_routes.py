from flask import Blueprint, request, jsonify
from models import Challenge, db
from datetime import datetime


# Blueprint with a prefix of /challenges
challenge_bp = Blueprint("challenge_bp", __name__, url_prefix="/challenges")


# ✅ Handles GET /challenges and GET /challenges/
@challenge_bp.route("", methods=["GET"])
@challenge_bp.route("/", methods=["GET"])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([c.to_dict() for c in challenges]), 200


# ✅ Get a single challenge by ID
@challenge_bp.route("/<int:id>", methods=["GET"])
def get_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    return jsonify(challenge.to_dict()), 200


# ✅ Create a new challenge
@challenge_bp.route("/", methods=["POST"])
def create_challenge():
    data = request.get_json()
    new_challenge = Challenge(
        name=data.get("name"),
        description=data.get("description"),
        created_by=data.get("created_by"),
        start_date=datetime.strptime(data.get("start_date"), "%Y-%m-%d").date() if data.get("start_date") else None,
        end_date=datetime.strptime(data.get("end_date"), "%Y-%m-%d").date() if data.get("end_date") else None,
    )
    db.session.add(new_challenge)
    db.session.commit()
    return jsonify(new_challenge.to_dict()), 201


# ✅ Update an existing challenge
@challenge_bp.route("/<int:id>", methods=["PATCH"])
def update_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    data = request.get_json()
    challenge.name = data.get("name", challenge.name)
    challenge.description = data.get("description", challenge.description)
    challenge.start_date = data.get("start_date", challenge.start_date)
    challenge.end_date = data.get("end_date", challenge.end_date)
    # Add other fields as needed
    db.session.commit()
    return jsonify(challenge.to_dict()), 200


# ✅ Delete a challenge
@challenge_bp.route("/<int:id>", methods=["DELETE"])
def delete_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    db.session.delete(challenge)
    db.session.commit()
    return jsonify({"message": "Challenge deleted"}), 200


# ✅ Test route (optional)
@challenge_bp.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Challenge route is working!"}), 200
