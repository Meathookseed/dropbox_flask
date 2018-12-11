from flask import request, jsonify, current_app
import jwt
from functools import wraps
from app.models.models import User

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Bearer' in request.headers:
            token = request.headers['Bearer']

        if not token:
            return jsonify({'message': 'Token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            print(data)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            print(current_user)
        except ValueError:
            return jsonify({'message': 'Token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorated
