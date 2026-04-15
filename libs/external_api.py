

import re

from flask_restx import Api

from pydantic import ValidationError

from flask import Flask, got_request_exception, Blueprint, current_app
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

from configs import app_config

def http_status_message(code):
    return HTTP_STATUS_CODES.get(code, "")

def register_external_error_handlers(api: Api):
    @api.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        # got_request_exception.send(current_app, exception=e)
        
        if e.response is not None:
            return e.response
        
        status_code = getattr(e, "code", 500) or 500
        
        # Build a safe, dict-like payload
        default_data = {
            "code": re.sub(r"(?<!^)(?=[A-Z])", "_", type(e).__name__).lower(),
            "message": getattr(e, "description", http_status_message(status_code)),
            "status": status_code,
        }
        
        if default_data["message"] == "Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)":
            default_data["message"] = "Invalid JSON payload received or JSON payload is empty."
            
        # Use headers on the exception if present; otherwise none.
        headers = {}
        exc_headers = getattr(e, "headers", None)
        if exc_headers:
            headers.update(exc_headers)
            
        # Payload per status
        if status_code == 406 and api.default_mediatype is None:
            data = {
                "code": "not_acceptable",
                "message": default_data["message"],
                "status": status_code,
            }
            return data, status_code, headers

        return default_data, status_code, headers

    _ = handle_http_exception
    
    @api.errorhandler(ValidationError) # actually it extend ValueError
    def handle_pydantic_validation_error(e: ValidationError):
        got_request_exception.send(current_app, exception=e)
        status_code = 422
        data = {
            "code": "validation_error",
            "message": "Request validation failed",
            "errors": e.errors(),
            "status": status_code,
        }
        return data, status_code
    
    _ = handle_pydantic_validation_error

    @api.errorhandler(ValueError)
    def handle_value_error(e: ValueError):
        got_request_exception.send(current_app, exception=e)
        status_code = 400
        data = {"code": "invalid_param", "message": str(e), "status": status_code}
        return data, status_code

    _ = handle_value_error

class ExternalApi(Api):
    
    _authorizations = {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Type: Bearer {your-api-key}"
        }
    }
    
    def __init__(
        self, app: Blueprint | Flask, *args, **kwargs
    ):
        kwargs.setdefault("authorizations", self._authorizations)
        kwargs.setdefault("security", "Bearer")
        kwargs["add_specs"] = app_config.SWAGGER_UI_ENABLED
        kwargs["doc"] = app_config.SWAGGER_UI_PATH if app_config.SWAGGER_UI_ENABLED else False
        
        # manual separate call on construction and init_app to ensure configs in kwargs effective
        super().__init__(app=None, *args, **kwargs)

        self.init_app(app, **kwargs)

        register_external_error_handlers(self)
