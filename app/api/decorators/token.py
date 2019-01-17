from app.models.models import User

from flask import request, make_response, current_app

from functools import wraps

import jwt


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'Bearer' in request.headers:
            token = request.headers['Bearer']

        if 'Bearer' in request.args:
            token = request.args.get('Bearer')

        if len(args) >= 2:
            token = args[1]

        if not token:
            return make_response('Token is invalid', 401)

        data = jwt.decode(token, current_app.config['SECRET_KEY'])

        current_user = User.query.filter_by(public_id=data['public_id']).first()

        return f(current_user, *args, **kwargs)
    return decorated
