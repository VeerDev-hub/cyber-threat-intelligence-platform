from flask import Blueprint, jsonify
from flask_login import login_required
from app.analytics.etl import process_raw_logs

analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


@analytics_bp.route("/process", methods=["POST"])
@login_required
def process_logs():
    count = process_raw_logs()
    return jsonify({
        "message": "ETL processing completed",
        "processed": count
    }), 200
