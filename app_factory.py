
import time
import logging
from flask import Flask

from configs import app_config
from contexts.wrapper import RecyclableContextVar

logger = logging.getLogger(__name__)


def create_flask_app_with_configs() -> Flask:
    """ 
    create a raw flask app
    with configs loaded from .env file
    """

    app = Flask(__name__)
    app.config.from_mapping(app_config.model_dump())

    # add before request hook
    @app.before_request
    def before_request():
        # add a unique identifier to each request
        RecyclableContextVar.increment_thread_recycles()

    _ = before_request

    return app


def create_app() -> Flask:

    start_time = time.perf_counter()
    app = create_flask_app_with_configs()
    initialize_extensions(app)
    end_time = time.perf_counter()
    if app_config.DEBUG:
        logger.info("Finished create_app (%s ms)", round(
            (end_time - start_time) * 1000, 2))

    return app


def initialize_extensions(app: Flask) -> None:
    from extensions import (
        ext_timezone,
        ext_logging,
        ext_warnings,
        ext_import_modules,
        ext_migrate,
        ext_orjson,
        ext_database,
        ext_app_metrics,
        ext_blueprints,
        ext_commands,
        ext_request_logging,
    )

    extensions = [
        ext_timezone,
        ext_logging,
        ext_warnings,
        ext_import_modules,
        ext_migrate,
        ext_orjson,
        ext_database,
        ext_app_metrics,
        ext_blueprints,
        ext_commands,
        ext_request_logging,
    ]

    for ext in extensions:
        short_name = ext.__name__.split(".")[-1]
        is_enabled = ext.is_enabled() if hasattr(ext, "is_enabled") else True
        if not is_enabled:
            if app_config.DEBUG:
                logger.info("Skipped %s", short_name)
            continue

        start_time = time.perf_counter()
        ext.init_app(app)
        end_time = time.perf_counter()
        if app_config.DEBUG:
            logger.info(
                "Loaded %s (%s ms)",
                short_name, round((end_time - start_time) * 1000, 2)
            )
