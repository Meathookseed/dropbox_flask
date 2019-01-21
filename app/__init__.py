from flask import Flask
from app.extensions import db, ma, migrate, docs, mail, cors, socket
from app.api.serializers.user import UserSchema
from app.api import (UserView, VaultView, LoginView, FileView, PhotoView, DataView, RegistrationView)
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

    elif os.environ.get('FLASK_ENV') == 'development' or app.config['TESTING'] is False:
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

    PhotoView.register(app, trailing_slash=True)
    docs.register(PhotoView, endpoint='PhotoView:put')

    LoginView.register(app, trailing_slash=True)
    docs.register(LoginView, endpoint='LoginView:post')

    RegistrationView.register(app, trailing_slash=True)
    docs.register(RegistrationView, endpoint='RegistrationView:post')

    UserView.register(app, trailing_slash=True)
    docs.register(UserView, endpoint='UserView:index')
    docs.register(UserView, endpoint='UserView:get')
    docs.register(UserView, endpoint='UserView:patch')
    docs.register(UserView, endpoint='UserView:delete')

    FileView.register(app, trailing_slash=True)
    docs.register(FileView, endpoint='FileView:index')
    docs.register(FileView, endpoint='FileView:get')
    docs.register(FileView, endpoint='FileView:post')
    docs.register(FileView, endpoint='FileView:patch')
    docs.register(FileView, endpoint='FileView:delete')

    VaultView.register(app, trailing_slash=True)
    docs.register(VaultView, endpoint='VaultView:index')
    docs.register(VaultView, endpoint='VaultView:get')
    docs.register(VaultView, endpoint='VaultView:patch')
    docs.register(VaultView, endpoint='VaultView:delete')
    docs.register(VaultView, endpoint='VaultView:post')

    DataView.register(app, trailing_slash=True)
    docs.register(DataView, endpoint='DataView:put')

    return app, socket
