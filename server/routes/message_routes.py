from flask_restful import Resource
from flask import request
from models import db, Message
from schemas import MessageSchema

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

class MessageListResource(Resource):
    def get(self):  # GET /messages
        messages = Message.query.filter_by(reply_to_id=None).order_by(Message.timestamp.desc()).all()
        return messages_schema.dump(messages), 200

    def post(self):  # POST /messages
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')
        reply_to_id = data.get('reply_to_id')

        if not user_id or not content:
            return {'error': 'Missing user_id or content'}, 400

        message = Message(user_id=user_id, content=content, reply_to_id=reply_to_id)
        db.session.add(message)
        db.session.commit()
        return message_schema.dump(message), 201