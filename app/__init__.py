from flask import Flask
from app.extensions import db, ma, migrate

from flask_cors import CORS
from app.api.users import UserView
from app.api.vault import VaultView
from app.api.login import LoginView
from from_yaml import YactConfig


def create_app():

    Flask.config_class = YactConfig
    app = Flask(__name__)
    app.config.from_yaml('config.yaml')

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    LoginView.register(app)
    UserView.register(app)
    VaultView.register(app)


    return app

