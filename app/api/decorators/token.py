from functools import wraps

import jwt

from flask import current_app, make_response, request

from app.models.models import User


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        try:
            if 'Bearer' in request.headers:
                token = request.headers['Bearer']

            elif 'token' in kwargs.keys():
                token = kwargs['token']

        except jwt.exceptions.DecodeError:
            return make_response('Token is invalid', 401)

        data = jwt.decode(token, current_app.config['SECRET_KEY'])

        current_user = User.query.filter_by(public_id=data['public_id']).first()

        return f(current_user, *args, **kwargs)
    return decorated
