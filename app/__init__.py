from flask import Flask
from app.extensions import db, ma, migrate, docs, mail, cors, socket
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
from sqlalchemy_utils import database_exists, create_database
import os


def create_app(config_file):

    Flask.config_class = YactConfig

    app = Flask(__name__)

    cors.init_app(app)

    socket.init_app(app)

    app.config.from_yaml(config_file)

    mail.init_app(app)

    if os.environ.get('FLASK_ENV') == 'docker':
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_url):
            create_database(db_url)

    elif os.environ.get('FLASK_ENV') == 'development' and app.config['TESTING'] is False \
            or os.environ.get('FLASK_ENV') is None:

        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_dropbox'
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    elif app.config['TESTING'] is True:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_flask_dropbox'
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    migrate.init_app(app, db)

    ma.init_app(app)

    docs.init_app(app)

    LoginView.register(app, trailing_slash=True)

    RegistrationView.register(app, trailing_slash=True)

    UserView.register(app, trailing_slash=True)

    PhotoView.register(app, trailing_slash=True)

    FileView.register(app, trailing_slash=True)

    VaultView.register(app, trailing_slash=True)

    DataView.register(app, trailing_slash=True)

    return app, socket
