from app.models.models import User

from flask import jsonify, make_response, current_app

import jwt

from werkzeug.security import check_password_hash
from flask import Response


class AuthService:

    @staticmethod
    def login(data: dict) -> Response:

        try:
            if not data or not data['username'] or not data['password']:
                return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})
        except KeyError:
            return make_response('Wrong data', 401)

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return make_response('Could not verify2', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

        if check_password_hash(user.password, data['password']):
            token = jwt.encode({'public_id': user.public_id},
                               current_app.config['SECRET_KEY'])

            return jsonify({'token': token.decode("UTF-8"), 'id': user.id})

        return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})
