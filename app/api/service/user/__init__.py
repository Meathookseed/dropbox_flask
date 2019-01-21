from app.api.decorators.token import token_required
from app.exceptions import UniqueUserAttributes
from app.models.models import User
from app.shortcuts import dbsession

from flask import jsonify, current_app, make_response, Response

from sqlalchemy.orm import Query

import uuid

import jwt

from werkzeug.security import generate_password_hash


class UserService:

    @staticmethod
    @token_required
    def list(current_user: User, **kwargs) -> Query:

        if not current_user.admin:
            return make_response('Forbidden', 403)

        users = User.query.all()

        return users

    @staticmethod
    @token_required
    def one(current_user: User, **kwargs) -> Query:

        if not current_user.id == int(kwargs['id']):

            return make_response('Forbidden', 403)

        user = User.query.filter_by(id=int(kwargs['id'])).first()

        return user

    @staticmethod
    def create(**kwargs) -> Response:

        data = kwargs['data']

        if not data:
            return make_response('No content', 204)

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

        return jsonify({'token': token.decode('utf-8'), 'id': new_user.id})

    @staticmethod
    @token_required
    def update(current_user: User, **kwargs) -> Response:

        if not kwargs['data']:
            return make_response('No content', 204)

        if not current_user.id == kwargs['id'] and not current_user.admin:
            return make_response('Forbidden', 403)

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

        return make_response('Updated', 200)

    @staticmethod
    @token_required
    def delete(current_user: User, **kwargs) -> Response:

        if not current_user.id == int(kwargs['id']) and not current_user.admin:
            return make_response('Forbidden', 403)

        user = User.query.filter_by(id=int(kwargs['id'])).first()

        dbsession.delete(user)

        dbsession.commit()

        return make_response('Deleted', 200)
