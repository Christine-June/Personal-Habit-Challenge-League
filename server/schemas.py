from flask_marshmallow import Marshmallow
from models import User, Habit, HabitEntry, Challenge, ChallengeEntry, ChallengeParticipant, Message

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True

    # Explicitly declare avatar_url so it shows up in output if needed
    avatar_url = ma.String()

class HabitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Habit
        load_instance = True

class HabitEntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HabitEntry
        load_instance = True

class ChallengeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Challenge
        load_instance = True

class ChallengeEntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChallengeEntry
        load_instance = True

class ChallengeParticipantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChallengeParticipant
        load_instance = True

class MessageSchema(ma.SQLAlchemyAutoSchema):
    username = ma.Function(lambda obj: obj.user.username if obj.user else None)
    avatar_url = ma.Function(lambda obj: obj.user.avatar_url if obj.user else None)
    
    class Meta:
        model = Message
        load_instance = True

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
