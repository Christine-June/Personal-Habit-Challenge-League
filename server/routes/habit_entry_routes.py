from flask import Blueprint, request, jsonify
from datetime import date
from functools import wraps
from models import HabitEntry, db

habit_entry_bp = Blueprint('habit_entries', __name__, url_prefix='/habit-entries')

def validate_habit_entry_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = request.get_json()

        required_fields = ['user_id', 'habit_id', 'progress']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {required_fields}'}), 400

        if not HabitEntry.validate_progress(data['progress']):
            return jsonify({'error': 'Invalid progress. Must be one of: completed, skipped, partial'}), 400

        if 'date' in data:
            try:
                data['parsed_date'] = date.fromisoformat(data['date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            data['parsed_date'] = date.today()

        return f(data, *args, **kwargs)
    return wrapper

@habit_entry_bp.route('/', methods=['POST'])
@validate_habit_entry_data
def create_habit_entry(data):
    new_entry = HabitEntry(
        user_id=data['user_id'],
        habit_id=data['habit_id'],
        progress=data['progress'],
        date=data['parsed_date'],
        notes=data.get('notes')
    )
    try:
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({
            'message': 'Habit entry created successfully',
            'entry': new_entry.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@habit_entry_bp.route('/', methods=['GET'])
def get_habit_entries():
    try:
        query = HabitEntry.query

        filters = {
            'user_id': request.args.get('user_id', type=int),
            'habit_id': request.args.get('habit_id', type=int),
            'progress': request.args.get('progress')
        }

        for key, value in filters.items():
            if value is not None:
                query = query.filter(getattr(HabitEntry, key) == value)

        if start_date := request.args.get('start_date'):
            start_date = date.fromisoformat(start_date)
            query = query.filter(HabitEntry.date >= start_date)

        if end_date := request.args.get('end_date'):
            end_date = date.fromisoformat(end_date)
            query = query.filter(HabitEntry.date <= end_date)

        entries = query.order_by(HabitEntry.date.desc()).all()
        return jsonify({
            'count': len(entries),
            'entries': [entry.to_dict() for entry in entries]
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@habit_entry_bp.route('/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_entry(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)

    if request.method == 'GET':
        return jsonify(entry.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()

        if 'progress' in data and not HabitEntry.validate_progress(data['progress']):
            return jsonify({'error': 'Invalid progress'}), 400

        if 'date' in data:
            try:
                entry.date = date.fromisoformat(data['date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format (use YYYY-MM-DD)'}), 400

        entry.progress = data.get('progress', entry.progress)
        entry.notes = data.get('notes', entry.notes)
        db.session.commit()
        return jsonify(entry.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Habit entry deleted successfully'})
