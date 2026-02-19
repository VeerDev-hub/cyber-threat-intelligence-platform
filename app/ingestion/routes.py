from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.raw_log import RawLog

ingestion_bp = Blueprint(
    "ingestion",
    __name__,
    url_prefix="/ingest"
)


@ingestion_bp.route("/logs", methods=["POST"])
@login_required
def ingest_logs():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    source = data.get("source")
    logs = data.get("logs")
    file_name = data.get("file_name")

    if not source or not logs or not isinstance(logs, list):
        return jsonify({"error": "Invalid log payload"}), 400

    created = 0

    for log_entry in logs:
        raw_log = RawLog(
            source=source,
            raw_data=log_entry,
            file_name=file_name,
            uploaded_by=current_user.id
        )
        db.session.add(raw_log)
        created += 1

    db.session.commit()

    return jsonify({
        "message": "Logs ingested successfully",
        "count": created
    }), 201
