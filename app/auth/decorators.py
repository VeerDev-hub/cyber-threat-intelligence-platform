from functools import wraps
from flask_login import current_user
from flask import jsonify


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "Authentication required"}), 401

            if current_user.role not in roles:
                return jsonify({"error": "Access denied"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
