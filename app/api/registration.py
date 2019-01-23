from app.api.service import UserService
from flask import make_response, jsonify
from flask_classful import FlaskView

from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, use_kwargs

from marshmallow import fields


class RegistrationView(FlaskView, metaclass=ResourceMeta):

    @use_kwargs({'username': fields.Str(),
                 'email': fields.Email(),
                 "password": fields.Str(),
                 })
    @doc(description='Creates new user')
    def post(self, **kwargs):
        """Create User"""

        result = UserService.create(data=kwargs)

        if result is False:
            return make_response('No data', 204)

        return jsonify({'token': result['token'].decode('utf-8'), 'id': result['user_id']})
