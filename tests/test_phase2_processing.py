import os

import pytest

from app import create_app
from app.analytics.etl import process_raw_logs
from app.extensions import db
from app.models.raw_log import RawLog
from app.models.processed_log import ProcessedLog
from app.models.user import User


@pytest.fixture()
def app():
    os.environ["DATABASE_URL"] = "sqlite:///test_phase2.db"
    app = create_app()
    app.config.update(TESTING=True)

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_process_raw_logs_persists_anomaly_fields(app):
    with app.app_context():
        user = User(username="phase2_user", email="phase2@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

        raw = RawLog(
            source="honeypot",
            raw_data={
                "timestamp": "2026-02-20T12:00:00",
                "src_ip": "10.0.0.5",
                "dst_ip": "10.0.0.9",
                "dst_port": 22,
                "protocol": "tcp",
                "message": "brute login attempt",
            },
            file_name="sample.json",
            uploaded_by=user.id,
        )
        db.session.add(raw)
        db.session.commit()

        count = process_raw_logs(limit=10)
        assert count == 1

        row = ProcessedLog.query.filter_by(raw_log_id=raw.id).first()
        assert row is not None
        assert row.anomaly_score is not None
        assert row.risk_level in {"low", "medium", "high"}
        assert isinstance(row.is_anomaly, bool)
