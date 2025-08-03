import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .config import settings
from .database import engine
from .database_data import seed_data
from .models import Base
from .routes import init_routes

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.update(settings.dict())

    csrf.init_app(app)

    with app.app_context():
        use_alembic = os.getenv("USE_ALEMBIC", "true").lower() == "true"

        if not use_alembic:
            from .database import drop_all_tables_cascade
            drop_all_tables_cascade()
            engine.echo = False
            Base.metadata.create_all(bind=engine)
            seed_data()
            engine.echo = True

    init_routes(app)

    return app
