from app.api.decorators.token import token_required
from app.exceptions import UniqueUserAttributes
from app.models.models import User
from app.shortcuts import dbsession

from flask import current_app

from sqlalchemy.orm import Query

import uuid

import jwt

from werkzeug.security import generate_password_hash


class UserService:

    @staticmethod
    @token_required
    def list(current_user: User, **kwargs) -> Query or None:

        if not current_user.admin:
            return None

        users = User.query.all()

        return users

    @staticmethod
    @token_required
    def one(current_user: User, **kwargs) -> Query or bool:

        if not current_user.id == int(kwargs['id']):

            return False

        user = User.query.filter_by(id=int(kwargs['id'])).first()

        return user

    @staticmethod
    def create(**kwargs) -> bool or dict:

        data = kwargs['data']

        if not data:
            return False

        try:
            data['admin']
        except KeyError:
            data['admin'] = True

        hashed_password = generate_password_hash(data['password'])

        inner_json = {
            'username': data['username'],
            'password': hashed_password,
            'admin': data['admin'],
            'email':  data['email'],

        }
        try:
            new_user = User(public_id=str(uuid.uuid4()),
                            username=inner_json['username'],
                            password=inner_json['password'],
                            admin=inner_json['admin'],
                            email=inner_json['email'],
                            )
            dbsession.add(new_user)
            dbsession.commit()

        except Exception:
            raise UniqueUserAttributes

        import tasks
        tasks.send_email.delay(inner_json)

        token = jwt.encode({'public_id': new_user.public_id},
                           current_app.config['SECRET_KEY'])

        return {'token': token, 'user_id': new_user.id}

    @staticmethod
    @token_required
    def update(current_user: User, **kwargs) -> bool or str:

        if bool(kwargs['data']) is False:
            return 'No data'

        if not current_user.id == kwargs['id'] and not current_user.admin:
            return False

        user = User.query.filter_by(id=int(kwargs['id'])).first()

        data = kwargs['data']

        if 'admin' in data:
            user.admin = data['admin']

        if 'email' in data:
            user.email = data['email']

        if 'password' in data:
            user.password = data['password']

        if 'username' in data:
            user.username = data['username']

        dbsession.commit()

        return True

    @staticmethod
    @token_required
    def delete(current_user: User, **kwargs) -> bool:

        if not current_user.id == int(kwargs['id']) and not current_user.admin:
            return False

        user = User.query.filter_by(id=int(kwargs['id'])).first()

        dbsession.delete(user)

        dbsession.commit()

        return True
