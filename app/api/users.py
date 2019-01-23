from app.api.service import UserService
from app.api.serializers import UserSchema
from flask import jsonify, make_response
from flask_classful import FlaskView
from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc, use_kwargs
from marshmallow import fields


@doc(tags=['User'])
class UserView(FlaskView, metaclass=ResourceMeta):

    DOCS_PARAMS_FOR_TOKEN = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                        "in": "header",
                                        "type": "string",
                                        "required": False}}

    @marshal_with(schema=UserSchema(), code='200')
    @doc(description='Get list of all users. ',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'},
         })
    def index(self, **kwargs):
        """Get list of all users."""

        result = UserService.list(**kwargs)

        if result is None:
            return make_response('No permission', 403)

        return jsonify({"users": UserSchema(many=True).dump(result).data})

    @marshal_with(schema=UserSchema(), code='200')
    @doc(description='Retrieve user by id. ',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'}
         })
    def get(self, id: int, **kwargs):
        """Retrieve one user."""

        result = UserService.one(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'user': UserSchema().dump(result).data})

    @use_kwargs({'admin': fields.Bool(),
                 'email': fields.Email(),
                 'password': fields.Str(),
                 'username': fields.Str(),
                 })
    @marshal_with(None)
    @doc(description='Updates user. ',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'},
             '200': {'description': 'User Updated'},
             '204': {'description': 'No data'}})
    def patch(self, id: int, **kwargs):
        """Update user"""

        result = UserService.update(data=kwargs, id=id)

        if result is True:
            return make_response('User updated', 200)
        elif result == 'No data':
            return make_response('No data', 204)
        elif result is False:
            return make_response('No permission', 403)

    @marshal_with(None)
    @doc(description='Deletes user. ',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '200': {'description': 'User deleted'},
             '403': {'description': 'No permission'}
         })
    def delete(self, id: int, **kwargs):
        """Delete User"""
        result = UserService.delete(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)
        elif result is True:
            return make_response('Deleted', 200)
