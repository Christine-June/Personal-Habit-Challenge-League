from flask import Blueprint, request, jsonify
from models import db, Message, User

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.filter_by(reply_to_id=None).order_by(Message.timestamp.desc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@message_bp.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    reply_to_id = data.get('reply_to_id')

    if not user_id or not content:
        return jsonify({'error': 'Missing user_id or content'}), 400

    message = Message(user_id=user_id, content=content, reply_to_id=reply_to_id)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201