from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from app.models.user import db, bcrypt


def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


# Create app instance for gunicorn
app = create_app() 