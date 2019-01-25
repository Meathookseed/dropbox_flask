import jwt
from flask import current_app
from werkzeug.security import check_password_hash

from app.models.models import User


class AuthService:

    @staticmethod
    def login(data: dict) -> str or dict:

        try:
            if not data or not data['username'] or not data['password']:
                return 'Wrong Data'
        except KeyError:
            return 'Wrong Data'

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return 'Wrong Data'

        if check_password_hash(user.password, data['password']):
            token = jwt.encode({'public_id': user.public_id},
                               current_app.config['SECRET_KEY'])

            return {'token': token.decode("UTF-8"), 'id': user.id}

        return 'Wrong Data'
