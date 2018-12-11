from flask_classy import FlaskView
from flask_apispec.annotations import marshal_with, doc
from flask import request

from app.api.service.user import UserService
from app.api.serializers.user import UserSchema


class UserView(FlaskView):

    @marshal_with(UserSchema(many=True))
    @doc(description='Get List of all users')
    def index(self):
        """List of users"""
        return UserService.list()


    @marshal_with(UserSchema())
    def get(self, public_id):
        """Retrieve one user"""
        return UserService.one(public_id)

    @doc(description='Creates new user')
    def post(self):
        """Create User"""
        data = request.get_json()
        return UserService.create(data)


    @doc(description='Updates user')
    @marshal_with(UserSchema())
    def patch(self, public_id):
        """Update user"""
        data = request.get_json()
        return UserService.update(data, public_id)

    @doc(description='Deletes user')
    def delete(self, public_id):
        """Delete User"""
        return UserService.delete(public_id)
