from app.api import bp
from flask import jsonify, request
from app.models import User
from app.api.utils.token import token_required
from app import db
from werkzeug.security import generate_password_hash
import jwt
import uuid
from app.api.serializers.user import UserSchema

@bp.route("/user", methods=['GET'])
@token_required
def user_list(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    user_schema = UserSchema(many=True)

    output = user_schema.dump(users).data

    return jsonify({'users': output})


@bp.route('/user', methods=['POST'])
def user_create():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'])

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
                    admin=False, email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'public_id': new_user.public_id},
                       bp.config['secret_key'])
    return jsonify({'token': token.decode("UTF-8")})


@bp.route('/user/<public_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def user_rud(current_user, public_id):

    if not current_user.admin and not current_user.public_id == public_id:
        return jsonify({'message': 'You have no permission'})

    if request.method == 'GET':

        if not current_user.admin and not current_user.public_id == public_id:
            return jsonify({'message': 'You have no permission'})

        user = User.query.filter_by(public_id=public_id).first()

        if not User:
            return jsonify({'message': 'There is no user'})

        user_data = dict()
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        user_data['password'] = user.password
        user_data['id'] = user.id

        return jsonify({'user': user_data})

    if request.method == 'PUT':

        data = request.get_json()

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message': 'There is no user'})

        if 'admin' in data:
            user.admin = data['admin']

        if 'email' in data:
            user.email = data['email']

        if 'password' in data:
            user.password = data['password']

        if 'username' in data:
            user.username = data['username']

        db.session.commit()

        return jsonify({'message': 'The user has been updated'})

    if request.method == 'DELETE':

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message': 'There is no user'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'The user has been deleted'})
