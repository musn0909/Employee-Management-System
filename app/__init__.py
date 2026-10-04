import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    if os.getenv("VERCEL"):
        app = Flask(
            __name__,
            instance_path="/tmp/employee_management_instance"
        )
    else:
        app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)

    from app.models import Employee
    from app.routes import main
    from app.api import api

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app