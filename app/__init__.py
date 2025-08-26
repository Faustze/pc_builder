import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config import settings
from app.database import engine
from app.database_data import seed_data
from app.models import Base
from app.routes import init_routes
from app.api import init_api


csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.update(settings.dict())

    csrf.init_app(app)
    init_api(app)

    with app.app_context():
        if os.getenv("USE_ALEMBIC", False):
            from app.database import drop_all_tables_cascade

            drop_all_tables_cascade()
            engine.echo = False
            Base.metadata.create_all(bind=engine)
            engine.echo = True

        engine.echo = False
        seed_data()

    init_routes(app)

    return app
