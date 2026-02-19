from flask import Blueprint

from .auth import auth_v1_bp
from .ingestion import ingestion_v1_bp
from .analytics import analytics_v1_bp


api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1_bp.register_blueprint(auth_v1_bp)
api_v1_bp.register_blueprint(ingestion_v1_bp)
api_v1_bp.register_blueprint(analytics_v1_bp)
