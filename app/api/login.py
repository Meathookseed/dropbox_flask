from app.api.service import AuthService
from flask import request

from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc

from flask_classful import FlaskView


class LoginView(FlaskView, metaclass=ResourceMeta):

    @doc(descrpiption='Login view')
    def post(self):
        data = request.get_json()

        return AuthService.login(data=data)


