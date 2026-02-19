from datetime import datetime
from app.extensions import db


class ProcessedLog(db.Model):
    __tablename__ = "processed_logs"

    id = db.Column(db.Integer, primary_key=True)

    raw_log_id = db.Column(
        db.Integer,
        db.ForeignKey("raw_logs.id"),
        nullable=False
    )

    timestamp = db.Column(db.DateTime, nullable=False)

    source_ip = db.Column(db.String(45), nullable=False)
    destination_ip = db.Column(db.String(45), nullable=True)

    destination_port = db.Column(db.Integer, nullable=True)

    protocol = db.Column(db.String(10), nullable=True)

    attack_type = db.Column(db.String(50), nullable=True)

    severity = db.Column(db.Integer, nullable=False)

    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)

    is_anomaly = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    processed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<ProcessedLog {self.id} severity={self.severity}>"
