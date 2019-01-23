from app.api.service import VaultService
from app.api.serializers import VaultSchema
from app.models.models import Vault
from flask import jsonify, make_response

from flask_classful import FlaskView, route

from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc, use_kwargs

from flask_sqlalchemy import BaseQuery

from marshmallow import fields


@doc(tags=['Vault'])
class VaultView(FlaskView, metaclass=ResourceMeta):

    DOCS_PARAMS_FOR_TOKEN = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                        "in": "header",
                                        "type": "string",
                                        "required": False}}

    @route('user_<id>/')
    @marshal_with(VaultSchema())
    @doc(description='Get List of all users vaults, <id> - user prop',
         params=DOCS_PARAMS_FOR_TOKEN)
    def index(self, id: int, **kwargs):
        """List of users"""

        result = VaultService.list(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'vaults': VaultSchema(many=True).dump(result).data})

    @marshal_with(VaultSchema())
    @doc(description='Retrieve one vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN)
    def get(self, id: int, **kwargs):
        """Retrieve one user"""

        result = VaultService.one(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'vault': VaultSchema().dump(result).data})

    @use_kwargs({'title': fields.Str(),
                 'description': fields.Str()})
    @doc(description='Creates vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN)
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
    @doc(description='Updates vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN)
    def patch(self, id: int, **kwargs):
        """Updates Vault"""

        result = VaultService.update(data=kwargs, id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result == 'No data':
            return make_response('No data', 204)
        elif result is True:
            return make_response('Updated', 200)

    @doc(description='Delete vault, <id> - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN)
    def delete(self, id: int):
        """Delete Vault"""

        result = VaultService.delete(id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result is True:
            return make_response('Deleted', 200)
