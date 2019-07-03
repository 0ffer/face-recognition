import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = (1, 0, 0, "dev")

db = SQLAlchemy()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # prepare DB location
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_file()

    # Prepare ORM
    db.init_app(app)
    db.app = app
    from src.models import User, Photo
    db.create_all(app=app)
    db.session.commit()

    # Prepare recognition context
    from src.recognition import update_context
    update_context()

    # Prepare serializer
    from src.serialization import CustomJSONEncoder
    app.json_encoder = CustomJSONEncoder

    # apply the blueprints to the app
    from src.api import bp

    app.register_blueprint(bp)

    return app


def get_database_file():
    project_dir = os.path.dirname(os.path.abspath(__file__))

    database_dir = os.path.join(project_dir, "data")
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

    database_file = "sqlite:///{}".format(os.path.join(database_dir, "database.db"))
    return database_file
