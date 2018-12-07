import os
basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(os.getcwd())+"/database.db"


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisissecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+file_path
    ADMINS = ['shokran1337@gmail.com']
    UPLOAD_FOLDER = os.path.join(basedir, 'upload')
    ALLOWED_EXTENSIONS = {('txt', 'pdf', 'png', 'jpg', 'jpeg', 'mp3', 'gif')}


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
