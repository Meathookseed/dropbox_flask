from flask_classy import FlaskView, route
from flask_apispec.annotations import marshal_with, doc
from flask import request
from app.api.service.user import UserService
from app.api.serializers.user import UserSchema
from app.api.service.photo import PhotoService

@marshal_with(UserSchema)
class UserView(FlaskView):

    @marshal_with(UserSchema(many=True))
    @doc(description='Get List of all users')
    def index(self):
        """List of users"""
        return UserService.list()

    @marshal_with(UserSchema)
    def get(self, id_):
        """Retrieve one user"""
        return UserService.one(id_)

    @doc(description='Updates user')
    @marshal_with(UserSchema)
    def patch(self, id_):
        """Update user"""
        data = request.get_json()
        return UserService.update(data, id_)

    @doc(description='Deletes user')
    def delete(self, id_):
        """Delete User"""
        return UserService.delete(id_)



