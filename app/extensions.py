from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mail import Mail
from flask_apispec import FlaskApiSpec
from flask_cors import CORS
from flask_socketio import SocketIO

db = SQLAlchemy()

migrate = Migrate(compare_type=True)

ma = Marshmallow()

docs = FlaskApiSpec()

mail = Mail()

socket = SocketIO()

cors = CORS(send_wildcard=False)