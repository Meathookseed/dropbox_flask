from app.api.service.user import UserService

from flask import request

from flask_classy import FlaskView

from flask_apispec.annotations import doc


class RegistrationView(FlaskView):

    @doc(description='Creates new user')
    def post(self):
        """Create User"""
        data = request.get_json()
        print(data)
        return UserService.create(data)
