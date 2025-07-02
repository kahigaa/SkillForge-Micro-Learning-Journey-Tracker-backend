from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from ..models import db, User, TokenBlocklist
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """Handles new user registration with username and email."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"msg": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already in use"}), 409
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    login_identifier = data.get('login')
    password = data.get('password')

    if not login_identifier or not password:
        return jsonify({"msg": "Username/email and password are required"}), 400

    user = User.query.filter(
        (User.username == login_identifier) | (User.email == login_identifier)
    ).first()

    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username/email or password"}), 401


@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout_user():
    """Logs out the user by adding their token to the blocklist."""
    jti = get_jwt()["jti"]
    now = datetime.utcnow()
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"msg": "Successfully logged out"}), 200

