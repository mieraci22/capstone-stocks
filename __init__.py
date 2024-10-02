from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize the extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/capstone'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname:port/dbname'

    # Initialize the extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from models import User  # Import the User model
    return app