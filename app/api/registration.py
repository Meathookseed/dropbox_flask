from flask import jsonify, make_response
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, use_kwargs
from flask_classful import FlaskView
from marshmallow import fields

from app.api.service import UserService


@doc(tags=['Authentication'])
class RegistrationView(FlaskView, metaclass=ResourceMeta):

    @use_kwargs({'username': fields.Str(),
                 'email': fields.Email(),
                 "password": fields.Str(),
                 })
    @doc(description='Creates new user',
         responses={'204': {'description': 'No data'}})
    def post(self, **kwargs):
        """Create User"""

        result = UserService.create(data=kwargs)

        if result is False:
            return make_response('No data', 204)

        return jsonify({'token': result['token'].decode('utf-8'), 'id': result['user_id']})
