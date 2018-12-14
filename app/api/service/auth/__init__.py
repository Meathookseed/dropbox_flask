from flask import jsonify, make_response, current_app
from werkzeug.security import check_password_hash
import jwt
from app.models.models import User


class AuthService:

    @staticmethod
    def login(data):

        if not data or not data['username'] or not data['password']:
            return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

        if check_password_hash(user.password, data['password']):
            token = jwt.encode({'public_id': user.public_id},
                               current_app.config['SECRET_KEY'])
            return jsonify({'token': token.decode("UTF-8"), 'id': user.id})

        return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})
