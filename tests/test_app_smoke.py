import os

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    os.environ["DATABASE_URL"] = "sqlite:///test_app.db"
    app = create_app()
    app.config.update(TESTING=True)

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cyber Threat Intelligence Platform is running." in response.data


def test_login_flow_and_dashboard(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "smoke_user",
            "email": "smoke@example.com",
            "password": "secret123",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"username": "smoke_user", "password": "secret123"},
    )
    assert login_response.status_code == 200

    dashboard_response = client.get("/dashboard/")
    assert dashboard_response.status_code == 200
