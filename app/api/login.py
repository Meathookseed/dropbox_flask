from flask import request
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, use_kwargs
from flask_classful import FlaskView
from marshmallow import fields

from app.api.service import AuthService


@doc(tags=['Authentication'])
class LoginView(FlaskView, metaclass=ResourceMeta):

    @use_kwargs({'username': fields.Str(), 'password': fields.Str()})
    @doc(descrpiption='Login view')
    def post(self, **kwargs):
        return AuthService.login(data=kwargs)
