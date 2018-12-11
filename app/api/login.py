from flask_classy import FlaskView
from flask_apispec.annotations import doc
from flask import request
from app.api.service.auth import AuthService


class LoginView(FlaskView):

    @doc(description='Login')
    def post(self):
        data = request.get_json()
        return AuthService.login(data)


