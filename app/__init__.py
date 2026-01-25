from dotenv import load_dotenv
load_dotenv()

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

from .config import DevelopmentConfig
from .extensions import db, login_manager, bcrypt, migrate
from app.auth.routes import auth_bp

from app.models.user import User
from app.models import raw_log, processed_log   
from app.ingestion.routes import ingestion_bp
from app.analytics.routes import analytics_bp




def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(analytics_bp)


    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Ensure logs directory exists
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Test DB connection (safe to keep for now)
    with app.app_context():
        try:
            db.engine.connect()
            app.logger.info("PostgreSQL connection successful")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")

    # Logging setup
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10240,
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Cyber Threat Intelligence Platform started")

    @app.route("/")
    def home():
        return "Cyber Threat Intelligence Platform is running."

    return app
