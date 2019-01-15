from app.models.models import User

from flask import request, jsonify, current_app

from functools import wraps

import jwt


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'Bearer' in request.headers:
            token = request.headers['Bearer']
        elif 'Bearer' in request.args:
            token = request.args.get('Bearer')

        if not token:
            return jsonify({'message': 'Token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])

            current_user = User.query.filter_by(public_id=data['public_id']).first()

        except ValueError:
            return jsonify({'message': 'Token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorated
