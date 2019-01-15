from app.api.service.user import UserService
from app.api.serializers.user import UserSchema
from app.models.models import User
from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_apispec.annotations import marshal_with, doc


class UserView(FlaskView):

    @marshal_with(UserSchema(many=True))
    @doc(description='Get List of all users')
    def index(self):
        """List of users"""

        response = UserService.list()

        if not isinstance(response, list):
            return response

        user_schema = UserSchema(many=True)

        user_result = user_schema.dump(response).data

        return jsonify({"users": user_result})

    @route('<id>/')
    @marshal_with(UserSchema)
    def get(self, id: int):
        """Retrieve one user"""

        response = UserService.one(id)

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
        return UserService.delete(id)
