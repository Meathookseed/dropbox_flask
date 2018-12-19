from flask import Flask
from app.extensions import db, ma, migrate, docs, cors
from flask_cors import CORS
from app.api.serializers.user import UserSchema
from app.api.users import UserView
from app.api.vault import VaultView
from app.api.login import LoginView
from app.api.file import FileView
from app.api.photo import PhotoView
from app.api.datafile import DataView
from app.api.registration import RegistrationView
from from_yaml import YactConfig
from app.api.service.file import FileService
import os

def create_app():

    Flask.config_class = YactConfig
    app = Flask(__name__)
    cors.init_app(app)
    app.config.from_yaml('config.yaml')
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    docs.init_app(app)
    LoginView.register(app)
    RegistrationView.register(app)
    UserView.register(app)
    PhotoView.register(app,trailing_slash=False)
    FileView.register(app, trailing_slash=False)
    VaultView.register(app, trailing_slash=False)
    DataView.register(app,trailing_slash=False)

    return app

