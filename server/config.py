import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secure-dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a-super-secret-jwt-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Standard local database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:password@localhost:5432/skillforge_dev'
    SQLALCHEMY_ECHO = False # Set to True to see all SQL queries

class ProductionConfig(Config):
    """Production configuration"""
    # Uses the DATABASE_URL from the deployment environment (e.g., Render)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Fix for Render/Heroku's postgres:// scheme
        uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        if uri and uri.startswith('postgres://'):
            app.config['SQLALCHEMY_DATABASE_URI'] = uri.replace('postgres://', 'postgresql://', 1)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
