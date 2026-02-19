from datetime import datetime
from app.extensions import db
from app.models.raw_log import RawLog
from app.models.processed_log import ProcessedLog


def calculate_severity(log: dict) -> int:
    message = str(log.get("message", "")).lower()
    port = log.get("dst_port")

    if "brute" in message:
        return 8
    if port == 22:
        return 6
    if "scan" in message:
        return 5

    return 3


def detect_attack_type(log: dict) -> str:
    message = str(log.get("message", "")).lower()

    if "brute" in message:
        return "brute_force"
    if "scan" in message:
        return "port_scan"

    return "unknown"


def process_raw_logs(limit: int = 100):
    raw_logs = (
        RawLog.query
        .filter_by(is_processed=False)
        .limit(limit)
        .all()
    )

    processed_count = 0

    for raw in raw_logs:
        data = raw.raw_data

        try:
            processed = ProcessedLog(
                raw_log_id=raw.id,
                timestamp=datetime.fromisoformat(
                    data.get("timestamp")
                ) if data.get("timestamp") else datetime.utcnow(),
                source_ip=data.get("src_ip"),
                destination_ip=data.get("dst_ip"),
                destination_port=data.get("dst_port"),
                protocol=data.get("protocol"),
                attack_type=detect_attack_type(data),
                severity=calculate_severity(data),
            )

            db.session.add(processed)
            raw.is_processed = True
            processed_count += 1

        except Exception:
            continue

    db.session.commit()
    return processed_count
