from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import db
from .routes import api

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app) # Enable CORS for frontend communication

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
