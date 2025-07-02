from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


from .user import User
from .journey import Journey
from .step import Step
from .user import TokenBlocklist