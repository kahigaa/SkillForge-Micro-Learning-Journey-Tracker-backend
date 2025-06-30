from flask import Blueprint, request, jsonify
from ..models import Journey, Step, db

journey_bp = Blueprint('journey', __name__, url_prefix='/api/journeys')

@journey_bp.route('/', methods=['GET'])
def get_all_journeys():
    """Get all journeys"""
    journeys = Journey.query.all()
    return jsonify([{
        'id': journey.id,
        'title': journey.title,
        'description': journey.description,
        'created_at': journey.created_at.isoformat(),
        'user_id': journey.user_id,
        'steps_count': journey.steps.count()
    } for journey in journeys])

@journey_bp.route('/<int:journey_id>', methods=['GET'])
def get_journey(journey_id):
    """Get a single journey with its steps"""
    journey = Journey.query.get_or_404(journey_id)
    return jsonify({
        'id': journey.id,
        'title': journey.title,
        'description': journey.description,
        'created_at': journey.created_at.isoformat(),
        'user_id': journey.user_id,
        'steps': [{
            'id': step.id,
            'title': step.title,
            'description': step.description,
            'is_complete': step.is_complete,
            'created_at': step.created_at.isoformat()
        } for step in journey.steps]
    })

@journey_bp.route('/', methods=['POST'])
def create_journey():
    """Create a new journey"""
    data = request.get_json()
    journey = Journey(
        title=data['title'],
        description=data.get('description'),
        user_id=data['user_id']
    )
    db.session.add(journey)
    db.session.commit()
    return jsonify({
        'id': journey.id,
        'title': journey.title,
        'message': 'Journey created successfully'
    }), 201

@journey_bp.route('/<int:journey_id>', methods=['PUT'])
def update_journey(journey_id):
    """Update a journey"""
    journey = Journey.query.get_or_404(journey_id)
    data = request.get_json()
    journey.title = data.get('title', journey.title)
    journey.description = data.get('description', journey.description)
    db.session.commit()
    return jsonify({
        'message': 'Journey updated successfully',
        'journey': {
            'id': journey.id,
            'title': journey.title
        }
    })

@journey_bp.route('/<int:journey_id>', methods=['DELETE'])
def delete_journey(journey_id):
    """Delete a journey (will cascade delete steps)"""
    journey = Journey.query.get_or_404(journey_id)
    db.session.delete(journey)
    db.session.commit()
    return jsonify({'message': 'Journey deleted successfully'})
