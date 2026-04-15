
from flask import Blueprint
from flask_restx import Namespace

from libs.external_api import ExternalApi

bp = Blueprint("service_api", __name__, url_prefix="/api")

api = ExternalApi(
    bp,
    version="1.0",
    title="Service API",
    description="API for application services",
)

service_api_ns = Namespace(
    "service_api", description="Service API operations", path="/")


api.add_namespace(service_api_ns)

__all__ = [
]
