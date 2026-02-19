from app.core.exceptions import ApiError


def validate_register_payload(payload):
    if not isinstance(payload, dict):
        raise ApiError("No input data provided", status_code=400, code="ValidationError")

    username = payload.get("username")
    email = payload.get("email")
    password = payload.get("password")

    if not username or not email or not password:
        raise ApiError(
            "Username, email, and password are required",
            status_code=400,
            code="ValidationError",
        )

    return {
        "username": str(username).strip(),
        "email": str(email).strip(),
        "password": str(password),
    }


def validate_login_payload(payload):
    if not isinstance(payload, dict):
        raise ApiError("No input data provided", status_code=400, code="ValidationError")

    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise ApiError(
            "Username and password are required",
            status_code=400,
            code="ValidationError",
        )

    return {
        "username": str(username).strip(),
        "password": str(password),
    }
