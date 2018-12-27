from app.api.decorators.token import token_required

from app.models.models import User
from app.shortcuts import dbsession

from flask import jsonify, current_app

import logging

import uuid

import jwt


from werkzeug.security import generate_password_hash


class UserService:

    def __init__(self):
        self.name = 'users'

    @staticmethod
    @token_required
    def list(current_user):

        if not current_user.admin and not current_user:
            return jsonify({'message': 'permission denied'})

        users = User.query.all()

        if not users:
            return jsonify({'message': "there is no users yet"})
        return users

    @staticmethod
    @token_required
    def one(current_user, id):

        if not current_user.id == int(id) and not current_user.admin and not current_user:
            return jsonify({'message': 'permission denied'})

        user = User.query.filter_by(id=int(id)).first()

        if not user:
            return jsonify({'message': "there is no users"})
        return user

    @staticmethod
    def create(data):

        hashed_password = generate_password_hash(data['password'])

        inner_json = {
            'username': data['username'],
            'password': hashed_password,
            'admin': True,
            'email':  data['email'],

        }
        new_user = User(public_id=str(uuid.uuid4()),
                            username=inner_json['username'],
                            password=inner_json['password'],
                            admin=inner_json['admin'],
                            email=inner_json['email'],
                            )
        dbsession.add(new_user)
        dbsession.commit()
        import tasks
        tasks.send_email.delay(inner_json)

        token = jwt.encode({'public_id': new_user.public_id},
                               current_app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('utf-8'), 'id': new_user.id})


    @staticmethod
    @token_required
    def update(data, current_user, id):

        if not current_user.id == int(id) and not current_user.admin:
            return jsonify({"message": "permission denied"})

        user = User.query.filter_by(id=int(id)).first()

        if not user:
            return jsonify({'message': "there is no user"})

        if 'admin' in data:
            user.admin = data['admin']

        if 'email' in data:
            user.email = data['email']

        if 'password' in data:
            user.password = data['password']

        if 'username' in data:
            user.username = data['username']

        dbsession.commit()

        return jsonify({'message': 'user updated'})

    @staticmethod
    @token_required
    def delete(current_user, id):

        if not current_user.id == int(id) and not current_user.admin:
            return jsonify({'message': "permission denied"})

        user = User.query.filter_by(id=int(id)).first()

        if not user:
            return jsonify({'message': "there is no user"})
        dbsession.delete(user)

        dbsession.commit()

        return jsonify({'message': 'user was deleted'})
