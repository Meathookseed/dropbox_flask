from app.api.service import VaultService
from app.api.serializers import VaultSchema

from flask import jsonify, make_response

from flask_classful import FlaskView, route

from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc, use_kwargs

from marshmallow import fields


@doc(tags=['Vault'])
class VaultView(FlaskView, metaclass=ResourceMeta):

    DOCS_PARAMS_FOR_TOKEN = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                        "in": "header",
                                        "type": "string",
                                        "required": False}}

    @route('user_<id>/')
    @marshal_with(VaultSchema(), code=200)
    @doc(description='Get List of all users vaults, <id> - user prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'}})
    def index(self, id: int, **kwargs):
        """List of users"""

        result = VaultService.list(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'vaults': VaultSchema(many=True).dump(result).data})

    @marshal_with(VaultSchema(), code=200)
    @doc(description='Retrieve one vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'}})
    def get(self, id: int, **kwargs):
        """Retrieve one user"""

        result = VaultService.one(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'vault': VaultSchema().dump(result).data})

    @use_kwargs({'title': fields.Str(),
                 'description': fields.Str()})
    @marshal_with(None)
    @doc(description='Creates vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'},
             '200': {'description': 'User Created'},
             '204': {'description': 'No data'}})
    def post(self, id: int, **kwargs):
        """Creates Vault"""
        result = VaultService.create(data=kwargs, id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result == 'No data':
            return make_response('No data', 204)
        elif result is True:
            return make_response('Created', 200)

    @use_kwargs({'title': fields.Str(),
                'description': fields.Str()})
    @marshal_with(None)
    @doc(description='Updates vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '403': {'description': 'No permission'},
             '200': {'description': 'Vault Updated'},
             '204': {'description': 'No data'}})
    def patch(self, id: int, **kwargs):
        """Updates Vault"""

        result = VaultService.update(data=kwargs, id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result == 'No data':
            return make_response('No data', 204)
        elif result is True:
            return make_response('Updated', 200)

    @marshal_with(None)
    @doc(description='Delete vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses={
             '200': {'description': 'User deleted'},
             '403': {'description': 'No permission'}})
    def delete(self, id: int):
        """Delete Vault"""

        result = VaultService.delete(id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result is True:
            return make_response('Deleted', 200)
