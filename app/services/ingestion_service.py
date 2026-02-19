from app.extensions import db
from app.models.raw_log import RawLog


def ingest_raw_logs(payload, uploaded_by):
    created = 0
    for log_entry in payload["logs"]:
        raw_log = RawLog(
            source=payload["source"],
            raw_data=log_entry,
            file_name=payload["file_name"],
            uploaded_by=uploaded_by,
        )
        db.session.add(raw_log)
        created += 1

    db.session.commit()
    return {"count": created}
