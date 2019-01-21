from app.api.service import UserService

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
        return UserService.create(data=kwargs)
