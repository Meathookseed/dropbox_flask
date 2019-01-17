from app.api.service import UserService

from flask import request

from flask_classful import FlaskView

from flask_apispec.annotations import doc


class RegistrationView(FlaskView):

    @doc(description='Creates new user')
    def post(self):
        """Create User"""
        data = request.get_json()
        return UserService.create(data)
