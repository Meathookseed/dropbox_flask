from flask import Flask
from app.extensions import db, ma, migrate
from config import Config
from flask_cors import CORS
from app.api.users import UserView


def create_app(config_class=Config):

    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    UserView.register(app, route_base='/')

    return app

