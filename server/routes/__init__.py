from flask import Blueprint
from flask_restful import Api

from .challenge_participant_routes import ChallengeParticipantList
from .challenge_entry_routes import ChallengeEntryList

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Register endpoints
api.add_resource(ChallengeParticipantList, "/challenge_participants")
api.add_resource(ChallengeEntryList, "/challenge_entries")
