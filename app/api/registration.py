from flask_classy import FlaskView
from app.api.service.user import UserService
from flask_apispec.annotations import doc
from flask import request


class RegistrationView(FlaskView):

    @doc(description='Creates new user')
    def post(self):
        """Create User"""
        data = request.get_json()
        print(data)
        return UserService.create(data)
