import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .config import settings
from .database import engine
from .database_data import seed_data
from .models import Base
from .routes import init_routes
from .api import init_api

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.update(settings.dict())

    csrf.init_app(app)
    init_api(app)

    with app.app_context():
        if os.getenv("USE_ALEMBIC", False):
            from .database import drop_all_tables_cascade

            drop_all_tables_cascade()
            engine.echo = False
            Base.metadata.create_all(bind=engine)
            engine.echo = True

        engine.echo = False
        seed_data()

    init_routes(app)

    return app
