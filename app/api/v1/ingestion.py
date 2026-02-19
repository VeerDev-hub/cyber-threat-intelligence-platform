from flask import Blueprint, request
from flask_login import login_required, current_user

from app.core.responses import success_response
from app.schemas.v1.ingestion import validate_ingestion_payload
from app.services.ingestion_service import ingest_raw_logs


ingestion_v1_bp = Blueprint("ingestion_v1", __name__, url_prefix="/ingest")


@ingestion_v1_bp.route("/logs", methods=["POST"])
@login_required
def ingest_logs():
    payload = validate_ingestion_payload(request.get_json(silent=True))
    result = ingest_raw_logs(payload=payload, uploaded_by=current_user.id)
    return success_response(
        data=result,
        message="Logs ingested successfully",
        status_code=201,
    )
