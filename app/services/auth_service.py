from flask_login import login_user as flask_login_user

from app.core.exceptions import ApiError
from app.extensions import db
from app.models.user import User


def register_user(payload):
    exists = User.query.filter(
        (User.username == payload["username"]) | (User.email == payload["email"])
    ).first()
    if exists:
        raise ApiError("User already exists", status_code=409, code="Conflict")

    user = User(username=payload["username"], email=payload["email"])
    user.set_password(payload["password"])
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}


def authenticate_user(payload):
    user = User.query.filter_by(username=payload["username"]).first()
    if not user or not user.check_password(payload["password"]):
        raise ApiError("Invalid credentials", status_code=401, code="Unauthorized")
    if not user.is_active:
        raise ApiError("Account is disabled", status_code=403, code="Forbidden")

    flask_login_user(user)
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }
