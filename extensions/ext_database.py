import logging

from flask import Flask

from models.engine import db

logger = logging.getLogger(__name__)

def init_app(app: Flask):
    
    db.init_app(app)
    
    # Eagerly build the engine so pool_size/max_overflow/etc. come from config
    try:
        with app.app_context():
            _ = db.engine  # triggers engine creation with the configured options
    except Exception:
        logger.exception(
            "Failed to initialize SQLAlchemy engine during app startup")
