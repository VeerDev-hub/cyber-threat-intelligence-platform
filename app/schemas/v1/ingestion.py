from app.core.exceptions import ApiError


def validate_ingestion_payload(payload):
    if not isinstance(payload, dict):
        raise ApiError("No input data provided", status_code=400, code="ValidationError")

    source = payload.get("source")
    logs = payload.get("logs")
    file_name = payload.get("file_name")

    if not source or not isinstance(logs, list) or len(logs) == 0:
        raise ApiError("Invalid log payload", status_code=400, code="ValidationError")

    return {
        "source": str(source).strip(),
        "logs": logs,
        "file_name": str(file_name).strip() if file_name else None,
    }
