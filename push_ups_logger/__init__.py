import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
import dropbox

load_dotenv()



# Initialize db here
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load the secret key from an environment variable
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'd98fe0facb0c6762ce0cf3e21b6fbdea6c94dc27152589420286212ade8474a9cd7c3aae958e5967d8e0a2013f43efd278c8f82ed7d3131201775e6a6e562bd5')

    # Other configurations and initializations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587  # For TLS
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

 # Your Gmail address
    

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    
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
