import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate 
from datetime import timedelta
from flask_cors import CORS

# Import config, db, and models
from .config import config
from .models import db, bcrypt, TokenBlocklist 

# Import controller Blueprints
from .controllers.auth_controller import auth_bp
from .controllers.journey_controller import journey_bp
from .controllers.step_controller import step_bp

def create_app(config_name=None):
    """Application Factory Pattern"""
    # Use production config on Render, otherwise default to development
    if os.getenv('RENDER'):
        config_name = 'production'
    elif config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # Configure CORS to allow requests from your frontend
    # For debugging, we'll allow all origins temporarily.
    # Remember to change this back to the specific list of origins later!
    CORS(app, origins="*", supports_credentials=True)

    # This function checks if a token has been revoked (logged out)
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None
    
    # Register all controller blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(journey_bp, url_prefix='/api/journeys')
    app.register_blueprint(step_bp, url_prefix='/api/steps')

    # A simple root route to confirm the API is running
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the SkillForge API!"})
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
