from flask import Blueprint, request, jsonify
from models import Challenge, db
from datetime import datetime

challenge_bp = Blueprint("challenge_bp", __name__, url_prefix="/challenges")

@challenge_bp.route("/", methods=["GET"])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([c.to_dict() for c in challenges]), 200

@challenge_bp.route("/<int:id>", methods=["GET"])
def get_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    return jsonify(challenge.to_dict()), 200



@challenge_bp.route("/", methods=["POST"])
def create_challenge():
    data = request.get_json()
    print("Received data:", data)

    try:
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date() if data.get("start_date") else None
        end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date() if data.get("end_date") else None

        if start_date and end_date and start_date > end_date:
            return jsonify({"error": "Start date must be before or equal to end date"}), 400

        new_challenge = Challenge(
            name=data["name"],
            description=data["description"],
            created_by=data["created_by"],
            start_date=start_date,
            end_date=end_date,
        )

        db.session.add(new_challenge)
        db.session.commit()
        return jsonify(new_challenge.to_dict()), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Invalid challenge data", "details": str(e)}), 400

# ✅ PATCH to update an existing challenge
@challenge_bp.route("/<int:id>", methods=["PATCH"])
def update_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        challenge.name = data["name"]
    if "description" in data:
        challenge.description = data["description"]
    if "created_by" in data:
        challenge.created_by = data["created_by"]
    if "start_date" in data:
        challenge.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    if "end_date" in data:
        challenge.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

    db.session.commit()
    return jsonify(challenge.to_dict()), 200

@challenge_bp.route("/<int:id>", methods=["DELETE"])
def delete_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    db.session.delete(challenge)
    db.session.commit()
    return jsonify({"message": "Challenge deleted"}), 200
