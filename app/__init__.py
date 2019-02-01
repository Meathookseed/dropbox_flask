import os

from flask import Flask
from sqlalchemy_utils import create_database, database_exists

from app.api import (DataView, FileView, LoginView, PhotoView,
                     RegistrationView, UserView, VaultView, ChargeView)
from app.api.serializers.user import UserSchema
from app.api.service.file import FileService
from app.extensions import cors, db, docs, ma, mail, migrate, socket

from from_yaml import YactConfig


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
            db.create_all()

    elif os.environ.get('FLASK_ENV') == 'development' or app.config['TESTING'] is False:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_dropbox'
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()

    elif app.config['TESTING'] is True:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_flask_dropbox'
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()

    db.init_app(app)

    migrate.init_app(app, db)

    ma.init_app(app)

    PhotoView.register(app, trailing_slash=True)

    LoginView.register(app, trailing_slash=True)

    RegistrationView.register(app, trailing_slash=True)

    UserView.register(app, trailing_slash=True)

    FileView.register(app, trailing_slash=True)

    VaultView.register(app, trailing_slash=True)

    DataView.register(app, trailing_slash=True)

    ChargeView.register(app, trailing_slash=True)

    if not app.config['TESTING']:
        docs.init_app(app)
        docs.register(PhotoView, endpoint='PhotoView:put')
        docs.register(LoginView, endpoint='LoginView:post')
        docs.register(RegistrationView, endpoint='RegistrationView:post')
        docs.register(UserView, endpoint='UserView:get')
        docs.register(UserView, endpoint='UserView:patch')
        docs.register(UserView, endpoint='UserView:delete')
        docs.register(UserView, endpoint='UserView:index')
        docs.register(FileView, endpoint='FileView:index')
        docs.register(FileView, endpoint='FileView:get')
        docs.register(FileView, endpoint='FileView:post')
        docs.register(FileView, endpoint='FileView:patch')
        docs.register(FileView, endpoint='FileView:delete')
        docs.register(VaultView, endpoint='VaultView:index')
        docs.register(VaultView, endpoint='VaultView:get')
        docs.register(VaultView, endpoint='VaultView:patch')
        docs.register(VaultView, endpoint='VaultView:delete')
        docs.register(VaultView, endpoint='VaultView:post')
        docs.register(DataView, endpoint='DataView:put')

    return app, socket
