from flask_restful import Resource
from flask import request
from datetime import date
from models import HabitEntry, db



class HabitEntryListResource(Resource):
    def get(self):  # GET /habit-entries
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
        return {
            'count': len(entries),
            'entries': habit_entries_schema.dump(entries)
        }, 200

    def post(self):  # POST /habit-entries
        data = request.get_json()
        required_fields = ['user_id', 'habit_id', 'progress']
        if not all(field in data for field in required_fields):
            return {'error': f'Missing required fields: {required_fields}'}, 400

        if not HabitEntry.validate_progress(data['progress']):
            return {'error': 'Invalid progress. Must be one of: completed, skipped, partial'}, 400

        entry_date = date.fromisoformat(data['date']) if 'date' in data else date.today()

        new_entry = HabitEntry(
            user_id=data['user_id'],
            habit_id=data['habit_id'],
            progress=data['progress'],
            date=entry_date,
            notes=data.get('notes')
        )
        try:
            db.session.add(new_entry)
            db.session.commit()
            return {
                'message': 'Habit entry created successfully',
                'entry': habit_entry_schema.dump(new_entry)
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class HabitEntryResource(Resource):
    def get(self, entry_id):  # GET /habit-entries/<id>
        entry = HabitEntry.query.get_or_404(entry_id)
        return habit_entry_schema.dump(entry), 200

    def put(self, entry_id):  # PUT /habit-entries/<id>
        entry = HabitEntry.query.get_or_404(entry_id)
        data = request.get_json()

        if 'progress' in data and not HabitEntry.validate_progress(data['progress']):
            return {'error': 'Invalid progress'}, 400

        if 'date' in data:
            try:
                entry.date = date.fromisoformat(data['date'])
            except ValueError:
                return {'error': 'Invalid date format (use YYYY-MM-DD)'}, 400

        entry.progress = data.get('progress', entry.progress)
        entry.notes = data.get('notes', entry.notes)
        db.session.commit()
        return habit_entry_schema.dump(entry), 200

    def delete(self, entry_id):  # DELETE /habit-entries/<id>
        entry = HabitEntry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        return {'message': 'Habit entry deleted successfully'}, 200
