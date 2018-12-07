from app import db
from flask import jsonify, current_app
from app.api.models.user import User
import uuid
from werkzeug.security import generate_password_hash
import jwt


class UserService:

    def __init__(self):
        self.name = 'users'

    @staticmethod
    def list():

        users = User.query.all()

        return users

    @staticmethod
    def one(id_):

        user = User.query.filter_by(id=id_).first()

        return user

    @staticmethod
    def create(data):

        public_id = str(uuid.uuid4())

        hashed_password = generate_password_hash(data['password'])

        inner_json = {
            'username': data['username'],
            'password': hashed_password,
            'admin': False,
            'email':  data['email']
        }

        new_user = User(public_id=public_id,
                        username=inner_json['username'],
                        password=inner_json['password'],
                        admin=inner_json['admin'],
                        email=inner_json['email'])

        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode({'public_id': new_user.public_id},
                           current_app.config['secret_key'])

        return token.decode("UTF-8")

    @staticmethod
    def update(data, id_):

        user = User.query.filter_by(id=id_).first()

        if 'admin' in data:
            user.admin = data['admin']

        if 'email' in data:
            user.email = data['email']

        if 'password' in data:
            user.password = data['password']

        if 'username' in data:
            user.username = data['username']

        db.session.commit()

        return user

    @staticmethod
    def delete(id_):

        user = User.query.filter_by(id=id_).first()

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'user was deleted'})

