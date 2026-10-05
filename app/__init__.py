import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app(config_overrides=None):

    if os.getenv("VERCEL"):
        app = Flask(
            __name__,
            instance_path="/tmp/employee_management_instance"
        )
    else:
        app = Flask(__name__)

    app.config.from_object(Config)

    # Apply test/development-specific configuration
    # BEFORE initializing SQLAlchemy.
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    from app.models import Employee, User
    from app.routes import main
    from app.api import api
    from app.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/api/auth")

    return app