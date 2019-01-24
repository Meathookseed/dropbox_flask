from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, use_kwargs, marshal_with
from flask_classful import FlaskView
from marshmallow import fields

from app.api.service import AuthService
from app.api.serializers.login import LoginSchema


@doc(tags=['Authentication'])
class LoginView(FlaskView, metaclass=ResourceMeta):

    @use_kwargs({'username': fields.Str(), 'password': fields.Str()})
    @marshal_with(LoginSchema())
    @doc(descrpiption='Login view')
    def post(self, **kwargs):
        return AuthService.login(data=kwargs)
