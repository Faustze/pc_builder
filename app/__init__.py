from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.api import init_api
from app.database import drop_all_tables_cascade, engine
from app.database_data import seed_data
from app.models import Base
from app.routes import init_routes

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    csrf.init_app(app)
    init_api(app)

    with app.app_context():
        drop_all_tables_cascade()
        Base.metadata.create_all(bind=engine)
        seed_data()

    init_routes(app)

    return app
