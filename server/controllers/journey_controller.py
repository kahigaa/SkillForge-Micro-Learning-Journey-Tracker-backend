from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Journey, Step, db  # Corrected relative import
from datetime import datetime

# The url_prefix is now handled in app.py during registration for clarity
journey_bp = Blueprint('journey_bp', __name__)


@journey_bp.route('/', methods=['GET'])
@jwt_required()  # <-- ADDED: This route now requires a valid token
def get_user_journeys():
    """Get all journeys for the currently logged-in user."""
    user_id = get_jwt_identity()  # <-- ADDED: Get the ID of the logged-in user
    journeys = Journey.query.filter_by(user_id=user_id).all() # <-- FIXED: Only get journeys for this user

    return jsonify([{
        'id': journey.id,
        'title': journey.title,
        'description': journey.description,
        'created_at': journey.created_at.isoformat(),
        'user_id': journey.user_id,
        'steps_count': journey.steps.count()
    } for journey in journeys])


@journey_bp.route('/<int:journey_id>', methods=['GET'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def get_journey(journey_id):
    """Get a single journey, ensuring it belongs to the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the ID of the logged-in user
    # <-- FIXED: Query now checks for both journey ID and user ID for security
    journey = Journey.query.filter_by(id=journey_id, user_id=user_id).first_or_404()
    
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
@jwt_required() # <-- ADDED: This route now requires a valid token
def create_journey():
    """Create a new journey for the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the ID of the logged-in user
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({"msg": "Missing title in request body"}), 400

    journey = Journey(
        title=data['title'],
        description=data.get('description'),
        user_id=user_id  # <-- FIXED: user_id now comes from the token, not the request body
    )
    db.session.add(journey)
    db.session.commit()
    
    return jsonify({
        'id': journey.id,
        'title': journey.title,
        'message': 'Journey created successfully'
    }), 201


@journey_bp.route('/<int:journey_id>', methods=['PUT'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def update_journey(journey_id):
    """Update a journey, ensuring it belongs to the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the ID of the logged-in user
    # <-- FIXED: Query now checks for both journey ID and user ID for security
    journey = Journey.query.filter_by(id=journey_id, user_id=user_id).first_or_404()
    
    data = request.get_json()
    journey.title = data.get('title', journey.title)
    journey.description = data.get('description', journey.description)
    db.session.commit()
    
    return jsonify({'message': 'Journey updated successfully'})


@journey_bp.route('/<int:journey_id>', methods=['DELETE'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def delete_journey(journey_id):
    """Delete a journey, ensuring it belongs to the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the ID of the logged-in user
    # <-- FIXED: Query now checks for both journey ID and user ID for security
    journey = Journey.query.filter_by(id=journey_id, user_id=user_id).first_or_404()
    
    db.session.delete(journey) # The 'cascade' in your model will delete the steps
    db.session.commit()
    
    return jsonify({'message': 'Journey deleted successfully'})