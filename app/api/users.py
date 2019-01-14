from app.api.service.user import UserService
from app.api.serializers.user import UserSchema

from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_apispec.annotations import marshal_with, doc


class UserView(FlaskView):

    @marshal_with(UserSchema(many=True))
    @doc(description='Get List of all users')
    def index(self):
        """List of users"""

        users = UserService.list()

        user_schema = UserSchema(many=True)

        user_result = user_schema.dump(users).data

        return jsonify({"users": user_result})

    @route('<id>/')
    @marshal_with(UserSchema)
    def get(self, id: int):
        """Retrieve one user"""

        user = UserService.one(id)

        user_schema = UserSchema()

        output = user_schema.dump(user).data

        return jsonify({'user': output})

    @doc(description='Updates user')
    def patch(self, id: int):
        """Update user"""
        data = request.get_json()

        return UserService.update(data=data, id=id)

    @doc(description='Deletes user')
    def delete(self, id: int):
        """Delete User"""
        return UserService.delete(id)
