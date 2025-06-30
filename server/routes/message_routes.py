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
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        reply_to_id = data.get('reply_to_id')

        if not sender_id or not receiver_id or not content:
            return {'error': 'Missing sender_id, receiver_id, or content'}, 400

        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            reply_to_id=reply_to_id
        )
        db.session.add(message)
        db.session.commit()
        return message_schema.dump(message), 201