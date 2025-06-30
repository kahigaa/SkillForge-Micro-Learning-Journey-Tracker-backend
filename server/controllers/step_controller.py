from flask import Blueprint, request, jsonify
from ..models import Step, db

step_bp = Blueprint('step', __name__, url_prefix='/api/steps')

@step_bp.route('/', methods=['POST'])
def create_step():
    """Create a new step for a journey"""
    data = request.get_json()
    step = Step(
        title=data['title'],
        description=data.get('description'),
        journey_id=data['journey_id']
    )
    db.session.add(step)
    db.session.commit()
    return jsonify({
        'id': step.id,
        'title': step.title,
        'message': 'Step created successfully'
    }), 201

@step_bp.route('/<int:step_id>', methods=['GET'])
def get_step(step_id):
    """Get a single step"""
    step = Step.query.get_or_404(step_id)
    return jsonify({
        'id': step.id,
        'title': step.title,
        'description': step.description,
        'is_complete': step.is_complete,
        'created_at': step.created_at.isoformat(),
        'journey_id': step.journey_id
    })

@step_bp.route('/<int:step_id>', methods=['PUT'])
def update_step(step_id):
    """Update a step"""
    step = Step.query.get_or_404(step_id)
    data = request.get_json()
    step.title = data.get('title', step.title)
    step.description = data.get('description', step.description)
    step.is_complete = data.get('is_complete', step.is_complete)
    db.session.commit()
    return jsonify({
        'message': 'Step updated successfully',
        'step': {
            'id': step.id,
            'title': step.title,
            'is_complete': step.is_complete
        }
    })

@step_bp.route('/<int:step_id>', methods=['DELETE'])
def delete_step(step_id):
    """Delete a step"""
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({'message': 'Step deleted successfully'})

@step_bp.route('/<int:step_id>/complete', methods=['PUT'])
def toggle_complete(step_id):
    """Toggle step completion status"""
    step = Step.query.get_or_404(step_id)
    step.is_complete = not step.is_complete
    db.session.commit()
    return jsonify({
        'message': 'Step completion status updated',
        'is_complete': step.is_complete
    })
