from app.api import bp
from flask import request, make_response, jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
from app.api.models.models import User


@bp.route('/login')
def login():

    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id},
                           current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode("UTF-8")})

    return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})
