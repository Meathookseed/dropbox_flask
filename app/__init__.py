from flask import Flask
from app.extensions import db, ma, migrate
from flask_apispec import FlaskApiSpec
from flask_cors import CORS
from app.api.users import UserView
from app.api.vault import VaultView
from app.api.login import LoginView
from app.api.file import FileView
from app.api.registration import RegistrationView
from from_yaml import YactConfig
from app.api.service.file import FileService

def create_app():

    Flask.config_class = YactConfig
    app = Flask(__name__)
    app.config.from_yaml('config.yaml')
    docs = FlaskApiSpec(app)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    LoginView.register(app)
    RegistrationView.register(app)
    UserView.register(app)
    docs.register(UserView)
    FileView.register(app, trailing_slash=False)
    VaultView.register(app, trailing_slash=False)

    return app

