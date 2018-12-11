from flask import jsonify, current_app, request, Response
from app.models.models import User
import uuid
from werkzeug.security import generate_password_hash
import jwt
from app.api.serializers.user import UserSchema
from app.shortcuts import dbsession
from app.api.decorators.token import token_required


class UserService:

    def __init__(self):
        self.name = 'users'

    @staticmethod
    @token_required
    def list(current_user):

        if not current_user.admin:
            return jsonify({'message': 'permission denied'})

        users = User.query.all()

        user_schema = UserSchema(many=True)

        user_result = user_schema.dump(users).data

        return jsonify({"users": user_result})

    @staticmethod
    @token_required
    def one(current_user, public_id):

        if not current_user.public_id == public_id and not current_user.admin:
            return jsonify({'message': 'permission denied'})

        user = User.query.filter_by(public_id=public_id).first()

        user_schema = UserSchema()

        output = user_schema.dump(user).data

        return jsonify({'user': output})

    @staticmethod
    def create(data):

        hashed_password = generate_password_hash(data['password'])

        inner_json = {
            'username': data['username'],
            'password': hashed_password,
            'admin': data['admin'],
            'email':  data['email']
        }
        
        new_user = User(public_id=str(uuid.uuid4()),
                        username=inner_json['username'],
                        password=inner_json['password'],
                        admin=inner_json['admin'],
                        email=inner_json['email'])

        dbsession.add(new_user)
        dbsession.commit()

        token = jwt.encode({'public_id': new_user.public_id},
                           current_app.config['SECRET_KEY'])

        return jsonify({'token': str(token)})

    @staticmethod
    @token_required
    def update(data, current_user, public_id):

        if not current_user.public_id == public_id and not current_user.admin:
            return jsonify({"message": "permission denied"})

        user = User.query.filter_by(public_id=public_id).first()

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
    def delete(current_user, public_id):

        if not current_user.public_id == public_id and not current_user.admin:
            return jsonify({'message': "permission denied"})

        user = User.query.filter_by(public_id=public_id).first()

        dbsession.delete(user)

        dbsession.commit()

        return jsonify({'message': 'user was deleted'})
