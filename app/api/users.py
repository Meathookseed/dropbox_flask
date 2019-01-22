from app.api.service import UserService
from app.api.serializers import UserSchema
from app.models.models import User
from flask import jsonify
from flask_classful import FlaskView
from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc, use_kwargs
from marshmallow import fields


@doc(tags=['user'])
class UserView(FlaskView, metaclass=ResourceMeta):

    @marshal_with(schema=UserSchema(many=True))
    @use_kwargs({'Bearer': fields.Str(required=True,
                                      description='Authorization HTTP header with JWT refresh token')},
                locations=['headers'])
    def index(self, **kwargs):
        """Get list of all users."""
        response = UserService.list(**kwargs)

        if not isinstance(response, list):
            return response

        user_schema = UserSchema(many=True)

        user_result = user_schema.dump(response).data

        return jsonify({"users": user_result})

    @marshal_with(schema=UserSchema())
    @use_kwargs({'Bearer': fields.Str(required=True,
                                      description='Authorization HTTP header with JWT refresh token')},
                locations=['headers'])
    def get(self, id: int, **kwargs):
        """Retrieve one user."""

        response = UserService.one(id=id, **kwargs)

        if not isinstance(response, User):
            return response

        user_schema = UserSchema()

        output = user_schema.dump(response).data

        return jsonify({'user': output})

    @use_kwargs({'admin': fields.Bool(),
                 'email': fields.Email(),
                 'password': fields.Str(),
                 'username': fields.Str(),
                 'token': fields.Str(required=False)})
    @doc(description='Updates user')
    def patch(self, id: int, **kwargs):
        """Update user"""
        return UserService.update(data=kwargs, id=id)

    @use_kwargs({'Bearer': fields.Str(required=True,
                                      description='Authorization HTTP header with JWT refresh token')},
                locations=['headers'])
    @doc(description='Deletes user')
    def delete(self, id: int):
        """Delete User"""
        return UserService.delete(id=id)
