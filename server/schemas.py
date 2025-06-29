from flask_marshmallow import Marshmallow
from models import User, Habit, Challenge, ChallengeParticipant, Message

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class HabitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Habit
        include_fk = True  # This ensures user_id is included
        load_instance = True

class ChallengeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Challenge
        include_fk = True  # <-- Add this line if not present
        load_instance = True

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)
challenge_schema = ChallengeSchema()
challenges_schema = ChallengeSchema(many=True)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)