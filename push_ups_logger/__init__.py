import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize db here
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load the secret key from an environment variable
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'd98fe0facb0c6762ce0cf3e21b6fbdea6c94dc27152589420286212ade8474a9cd7c3aae958e5967d8e0a2013f43efd278c8f82ed7d3131201775e6a6e562bd5')

    # Other configurations and initializations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app
