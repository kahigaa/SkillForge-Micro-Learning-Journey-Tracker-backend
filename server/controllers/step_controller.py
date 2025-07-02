from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Step, Journey, db  # Corrected relative import
from datetime import datetime

step_bp = Blueprint('step_bp', __name__)

@step_bp.route('/', methods=['POST'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def create_step():
    """Create a new step for a journey"""
    user_id = get_jwt_identity() # <-- ADDED: Get the logged-in user's ID
    data = request.get_json()

    # --- FIX STARTS HERE ---
    # Validate that the necessary data was sent
    if not data or not data.get('title') or not data.get('journey_id'):
        return jsonify({"msg": "Missing title or journey_id in request body"}), 400

    # Verify that the user owns the journey they are adding a step to
    journey_id = data['journey_id']
    journey = Journey.query.filter_by(id=journey_id, user_id=user_id).first()
    if not journey:
        return jsonify({"msg": "Journey not found or you don't have permission to access it"}), 404
    # --- FIX ENDS HERE ---

    step = Step(
        title=data['title'],
        description=data.get('description'),
        journey_id=journey_id
    )
    db.session.add(step)
    db.session.commit()
    
    return jsonify({
        'id': step.id,
        'title': step.title,
        'message': 'Step created successfully'
    }), 201

@step_bp.route('/<int:step_id>', methods=['GET'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def get_step(step_id):
    """Get a single step, ensuring it belongs to the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the logged-in user's ID
    # <-- FIXED: Query now checks that the step belongs to one of the user's journeys
    step = db.session.query(Step).join(Journey).filter(
        Step.id == step_id,
        Journey.user_id == user_id
    ).first_or_404()
    
    return jsonify({
        'id': step.id,
        'title': step.title,
        'description': step.description,
        'is_complete': step.is_complete
    })

@step_bp.route('/<int:step_id>', methods=['PUT'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def update_step(step_id):
    """Update a step, ensuring it belongs to the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the logged-in user's ID
    # <-- FIXED: Query now checks that the step belongs to one of the user's journeys
    step = db.session.query(Step).join(Journey).filter(
        Step.id == step_id,
        Journey.user_id == user_id
    ).first_or_404()

    data = request.get_json()
    step.title = data.get('title', step.title)
    step.description = data.get('description', step.description)
    step.is_complete = data.get('is_complete', step.is_complete)
    db.session.commit()
    
    return jsonify({'message': 'Step updated successfully'})

@step_bp.route('/<int:step_id>', methods=['DELETE'])
@jwt_required() # <-- ADDED: This route now requires a valid token
def delete_step(step_id):
    """Delete a step, ensuring it belongs to the logged-in user."""
    user_id = get_jwt_identity() # <-- ADDED: Get the logged-in user's ID
    # <-- FIXED: Query now checks that the step belongs to one of the user's journeys
    step = db.session.query(Step).join(Journey).filter(
        Step.id == step_id,
        Journey.user_id == user_id
    ).first_or_404()
    
    db.session.delete(step)
    db.session.commit()
    
    return jsonify({'message': 'Step deleted successfully'})

@step_bp.route('/<int:step_id>/complete', methods=['PUT'])
@jwt_required()
def toggle_complete(step_id):
    """Toggle step completion status"""
    user_id = get_jwt_identity()
    step = db.session.query(Step).join(Journey).filter(
        Step.id == step_id,
        Journey.user_id == user_id
    ).first_or_404()

    step.is_complete = not step.is_complete
    db.session.commit()
    
    return jsonify({
        'message': 'Step completion status updated',
        'is_complete': step.is_complete
    })