from flask import jsonify, make_response
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, marshal_with, use_kwargs
from flask_classful import FlaskView, route
from marshmallow import fields

from app.api.serializers import VaultSchema
from app.api.service import VaultService
from app.openapi_doc_parameters import *


@doc(tags=['Vault'])
class VaultView(FlaskView, metaclass=ResourceMeta):

    @route('user_<id>/')
    @marshal_with(VaultSchema(), code='200')
    @doc(description='Get List of all users vaults, id - user prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=GET_CODES)
    def index(self, id: int, **kwargs):
        """List of users"""

        result = VaultService.list(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'vaults': VaultSchema(many=True).dump(result).data})

    @marshal_with(VaultSchema(), code='200')
    @doc(description='Retrieve one vault, id - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=GET_CODES)
    def get(self, id: int, **kwargs):
        """Retrieve one user"""

        result = VaultService.one(id=id, **kwargs)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'vault': VaultSchema().dump(result).data})

    @use_kwargs({'title': fields.Str(),
                 'description': fields.Str()})
    @marshal_with(None)
    @doc(description='Creates vault, id - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=POST_CODES)
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
    @doc(description='Updates vault, id - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=PATCH_CODES)
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
    @doc(description='Delete vault, id - vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=DELETE_CODES)
    def delete(self, id: int):
        """Delete Vault"""

        result = VaultService.delete(id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result is True:
            return make_response('Deleted', 200)
