from flask import Blueprint
from flask_restx import Api

from .assemblies import assemblies_ns
from .classificators import classificators_ns
from .components import components_ns


def init_api(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")
    api = Api(
        api_bp,
        version="1.0",
        title="PC Components API",
        description="API для управления компонентами компьютера и сборками",
        doc="/",
    )

    api.add_namespace(components_ns, path="/components")
    api.add_namespace(classificators_ns, path="/classificators")
    api.add_namespace(assemblies_ns, path="/assemblies")

    app.register_blueprint(api_bp)
