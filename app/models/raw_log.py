from datetime import datetime
from app.extensions import db


class RawLog(db.Model):
    __tablename__ = "raw_logs"

    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.String(50), nullable=False)

    raw_data = db.Column(db.JSON, nullable=False)

    file_name = db.Column(db.String(255), nullable=True)

    ingested_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    is_processed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __repr__(self):
        return f"<RawLog {self.id} from {self.source}>"
