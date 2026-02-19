from flask import request
from werkzeug.exceptions import HTTPException

from app.core.exceptions import ApiError
from app.core.responses import error_response

def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        if request.path.startswith("/api/"):
            return error_response(
                message=error.message,
                code=error.code,
                status_code=error.status_code,
                details=error.details,
            )
        raise error

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        if request.path.startswith("/api/"):
            return error_response(
                message=error.description,
                code=error.name,
                status_code=error.code,
            )
        return error

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        if request.path.startswith("/api/"):
            app.logger.exception("Unhandled API exception")
            return error_response(
                message="Unexpected server error",
                code="InternalServerError",
                status_code=500,
            )
        raise error
