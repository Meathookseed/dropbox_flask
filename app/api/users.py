from app.api.service import UserService
from app.api.serializers import UserSchema
from app.models.models import User
from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc


@doc(description='All User Endpoints', tags=['user'])
class UserView(FlaskView, metaclass=ResourceMeta):

    @marshal_with(schema=UserSchema(many=True))
    @doc(description='Get List of all users',inherit=None)
    def index(self):
        """Get list of all users."""
        response = UserService.list()

        if not isinstance(response, list):
            return response

        user_schema = UserSchema(many=True)

        user_result = user_schema.dump(response).data

        return jsonify({"users": user_result})

    @marshal_with(schema=UserSchema())
    @doc(description='Retrieve one user')
    def get(self, id: int):
        """Retrieve one user."""
        response = UserService.one(id=id)

        if not isinstance(response, User):
            return response

        user_schema = UserSchema()

        output = user_schema.dump(response).data

        return jsonify({'user': output})

    @doc(description='Updates user')
    def patch(self, id: int):
        """Update user"""
        data = request.get_json()

        return UserService.update(data=data, id=id)

    @doc(description='Deletes user')
    def delete(self, id: int):
        """Delete User"""
        return UserService.delete(id=id)
