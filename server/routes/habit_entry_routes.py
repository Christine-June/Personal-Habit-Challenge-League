from flask import Blueprint, request, jsonify
from datetime import datetime, date
from functools import wraps
from models import db, HabitEntry

habit_entry_bp = Blueprint('habit_entries', __name__, url_prefix='/habit-entries')

def validate_habit_entry_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        
        # Required field validation
        required_fields = ['user_id', 'habit_id', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
            
        # Status validation
        if not HabitEntry.validate_status(data['status']):
            return jsonify({'error': 'Invalid status. Must be one of: completed, skipped, partial'}), 400
            
        # Date validation
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
    """
    Create a new habit entry
    ---
    tags:
      - Habit Entries
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - habit_id
            - status
          properties:
            user_id:
              type: integer
            habit_id:
              type: integer
            status:
              type: string
              enum: [completed, skipped, partial]
            date:
              type: string
              format: date
            notes:
              type: string
    responses:
      201:
        description: Habit entry created
      400:
        description: Invalid input
    """
    new_entry = HabitEntry(
        user_id=data['user_id'],
        habit_id=data['habit_id'],
        status=data['status'],
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
    """
    Get filtered habit entries
    ---
    tags:
      - Habit Entries
    parameters:
      - in: query
        name: user_id
        type: integer
      - in: query
        name: habit_id
        type: integer
      - in: query
        name: status
        type: string
        enum: [completed, skipped, partial]
      - in: query
        name: start_date
        type: string
        format: date
      - in: query
        name: end_date
        type: string
        format: date
    responses:
      200:
        description: List of habit entries
      400:
        description: Invalid date format
    """
    try:
        query = HabitEntry.query
        
        # Filter parameters
        filters = {
            'user_id': request.args.get('user_id', type=int),
            'habit_id': request.args.get('habit_id', type=int),
            'status': request.args.get('status')
        }
        
        for key, value in filters.items():
            if value is not None:
                query = query.filter(getattr(HabitEntry, key) == value)
                
        # Date range filtering
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
        
        if 'status' in data and not HabitEntry.validate_status(data['status']):
            return jsonify({'error': 'Invalid status'}), 400
        
        if 'date' in data:
            try:
                entry.date = date.fromisoformat(data['date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format (use YYYY-MM-DD)'}), 400
        
        entry.status = data.get('status', entry.status)
        entry.notes = data.get('notes', entry.notes)
        db.session.commit()
        return jsonify(entry.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Habit entry deleted successfully'})
