from dotenv import load_dotenv
load_dotenv()

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os
from .config import DevelopmentConfig
from .extensions import db, login_manager, bcrypt, migrate

from app.models.user import User
from app.models import raw_log, processed_log   
from app.auth.routes import auth_bp
from app.ingestion.routes import ingestion_bp
from app.analytics.routes import analytics_bp
from app.dashboards.routes import dashboard_bp
from app.api.v1 import api_v1_bp
from app.core.errors import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_v1_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    register_error_handlers(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    if not os.path.exists("logs"):
        os.mkdir("logs")

    with app.app_context():
        try:
            with db.engine.connect():
                backend = db.engine.url.get_backend_name()
                app.logger.info(f"Database connection successful ({backend})")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")

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
