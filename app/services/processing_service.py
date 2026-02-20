from datetime import datetime

from app.extensions import db
from app.models.raw_log import RawLog
from app.models.processed_log import ProcessedLog
from app.services.detectors.ml_detector import MLDetector


def calculate_severity(log):
    message = str(log.get("message", "")).lower()
    port = log.get("dst_port")

    if "brute" in message:
        return 8
    if port == 22:
        return 6
    if "scan" in message:
        return 5
    return 3


def detect_attack_type(log):
    message = str(log.get("message", "")).lower()

    if "brute" in message:
        return "brute_force"
    if "scan" in message:
        return "port_scan"
    return "unknown"


def _parse_timestamp(value):
    if not value:
        return datetime.utcnow()
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return datetime.utcnow()


def process_pending_raw_logs(limit=100, detector=None):
    if detector is None:
        detector = MLDetector()

    raw_logs = RawLog.query.filter_by(is_processed=False).limit(limit).all()
    processed_count = 0

    for raw in raw_logs:
        data = raw.raw_data or {}

        try:
            severity = calculate_severity(data)
            attack_type = detect_attack_type(data)
            detection = detector.detect(
                {
                    "severity": severity,
                    "destination_port": data.get("dst_port"),
                    "attack_type": attack_type,
                    "source_ip": data.get("src_ip"),
                    "timestamp": data.get("timestamp"),
                }
            )

            processed = ProcessedLog(
                raw_log_id=raw.id,
                timestamp=_parse_timestamp(data.get("timestamp")),
                source_ip=data.get("src_ip"),
                destination_ip=data.get("dst_ip"),
                destination_port=data.get("dst_port"),
                protocol=data.get("protocol"),
                attack_type=attack_type,
                severity=severity,
                anomaly_score=detection.anomaly_score,
                is_anomaly=detection.is_anomaly,
                risk_level=detection.risk_level,
            )

            db.session.add(processed)
            raw.is_processed = True
            processed_count += 1
        except Exception:
            continue

    db.session.commit()
    return processed_count
