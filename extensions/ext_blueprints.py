
from flask.app import Flask

from constants import HEADER_NAME_APP_CODE, HEADER_NAME_CSRF_TOKEN, HEADER_NAME_PASSPORT

from configs import app_config

BASE_CORS_HEADERS: tuple[str, ...] = (
    "Content-Type", HEADER_NAME_APP_CODE, HEADER_NAME_PASSPORT)
SERVICE_API_HEADERS: tuple[str, ...] = (*BASE_CORS_HEADERS, "Authorization")
AUTHENTICATED_HEADERS: tuple[str, ...] = (
    *SERVICE_API_HEADERS, HEADER_NAME_CSRF_TOKEN)

def init_app(app: Flask):
    
    from flask_cors import CORS

    from controllers.console import bp as console_app_bp

    CORS(
        console_app_bp,
        resources={r"/*": {"origins": app_config.CONSOLE_CORS_ALLOW_ORIGINS}},
        supports_credentials=True,
        allow_headers=list(AUTHENTICATED_HEADERS),
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["X-Version", "X-Env"],
    )
    app.register_blueprint(console_app_bp)
    
    from controllers.service_api import bp as service_api_bp
    
    app.register_blueprint(service_api_bp)