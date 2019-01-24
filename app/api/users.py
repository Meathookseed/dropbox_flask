from flask import jsonify, make_response
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, marshal_with, use_kwargs
from flask_classful import FlaskView
from marshmallow import fields

from app.api.serializers import UserSchema
from app.api.service import UserService
from app.openapi_doc_parameters import *


@doc(tags=['User'])
class UserView(FlaskView, metaclass=ResourceMeta):

    @marshal_with(schema=UserSchema(), code='200')
    @doc(description='Get list of all users. ',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=GET_CODES)
    def index(self, **kwargs):
        """Get list of all users."""

        result = UserService.list(**kwargs)

        if result is False:
            return make_response('No permission', 403)
        else:
            return jsonify({"users": UserSchema(many=True).dump(result).data})

    @marshal_with(schema=UserSchema(), code='200')
    @doc(description='Retrieve user by id. ',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=GET_CODES)
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
         responses=PATCH_CODES)
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
         responses=DELETE_CODES)
    def delete(self, id: int, **kwargs):
        """Delete User"""
        result = UserService.delete(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)
        elif result is True:
            return make_response('Deleted', 200)
