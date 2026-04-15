from importlib import import_module
from flask import Blueprint
from flask_restx import Namespace

from libs.external_api import ExternalApi

bp = Blueprint("console", __name__, url_prefix="/console/api")

api = ExternalApi(
    bp,
    version="1.0",
    title="Console API",
    description="Console management APIs for app configuration, monitoring, and administration.",
)

console_ns = Namespace(
    "console", description="Console management API operations", path="/"
)
RESOURCE_MODULES = (
)

for module_name in RESOURCE_MODULES:
    import_module(module_name)

api.add_namespace(console_ns)

__all__ = [
    
]
