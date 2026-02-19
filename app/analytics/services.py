from sqlalchemy import func
from app.extensions import db
from app.models.processed_log import ProcessedLog


def summary_metrics():
    total_attacks = db.session.query(func.count(ProcessedLog.id)).scalar()

    avg_severity = db.session.query(
        func.avg(ProcessedLog.severity)
    ).scalar()

    severity_distribution = (
        db.session.query(
            ProcessedLog.severity,
            func.count(ProcessedLog.id)
        )
        .group_by(ProcessedLog.severity)
        .order_by(ProcessedLog.severity)
        .all()
    )

    return {
        "total_attacks": total_attacks or 0,
        "average_severity": round(float(avg_severity), 2) if avg_severity else 0,
        "severity_distribution": [
            {"severity": s, "count": c}
            for s, c in severity_distribution
        ]
    }


def top_attacker_ips(limit=5):
    rows = (
        db.session.query(
            ProcessedLog.source_ip,
            func.count(ProcessedLog.id).label("count")
        )
        .group_by(ProcessedLog.source_ip)
        .order_by(func.count(ProcessedLog.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {"source_ip": ip, "count": count}
        for ip, count in rows
    ]


def top_target_ports(limit=5):
    rows = (
        db.session.query(
            ProcessedLog.destination_port,
            func.count(ProcessedLog.id).label("count")
        )
        .filter(ProcessedLog.destination_port.isnot(None))
        .group_by(ProcessedLog.destination_port)
        .order_by(func.count(ProcessedLog.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {"port": port, "count": count}
        for port, count in rows
    ]


def attack_types_distribution():
    rows = (
        db.session.query(
            ProcessedLog.attack_type,
            func.count(ProcessedLog.id)
        )
        .group_by(ProcessedLog.attack_type)
        .all()
    )

    return [
        {"attack_type": atype, "count": count}
        for atype, count in rows
    ]
