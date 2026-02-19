from flask import Blueprint, request
from flask_login import logout_user, login_required

from app.auth.decorators import role_required
from app.core.responses import success_response
from app.schemas.v1.auth import validate_register_payload, validate_login_payload
from app.services.auth_service import register_user, authenticate_user


auth_v1_bp = Blueprint("auth_v1", __name__, url_prefix="/auth")


@auth_v1_bp.route("/register", methods=["POST"])
def register():
    payload = validate_register_payload(request.get_json(silent=True))
    user_data = register_user(payload)
    return success_response(
        data={"user": user_data},
        message="User registered successfully",
        status_code=201,
    )


@auth_v1_bp.route("/login", methods=["POST"])
def login():
    payload = validate_login_payload(request.get_json(silent=True))
    user_data = authenticate_user(payload)
    return success_response(
        data={"user": user_data},
        message="Login successful",
        status_code=200,
    )


@auth_v1_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return success_response(message="Logged out successfully", status_code=200)


@auth_v1_bp.route("/admin-only", methods=["GET"])
@role_required("admin")
def admin_only():
    return success_response(message="Welcome admin", status_code=200)
