from app.api.service import VaultService
from app.api.serializers import VaultSchema
from app.models.models import Vault
from flask import request, jsonify

from flask_classful import FlaskView, route

from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc, use_kwargs

from flask_sqlalchemy import BaseQuery

from marshmallow import fields


class VaultView(FlaskView, metaclass=ResourceMeta):

    @route('user_<id>/')
    @marshal_with(VaultSchema(many=True))
    @doc(description='Get List of all users vaults, <id> - user prop')
    def index(self, id: int):
        """List of users"""

        response = VaultService.list(id=id)

        if not isinstance(response, BaseQuery):
            return response

        schema = VaultSchema(many=True)

        output = schema.dump(response).data

        return jsonify({'vaults': output})

    @marshal_with(VaultSchema())
    @doc(description='Retrieve one vault, <id> - vault prop')
    def get(self, id: int):
        """Retrieve one user"""

        vault = VaultService.one(id=id)

        if not isinstance(vault, Vault):
            return vault

        schema = VaultSchema()

        output = schema.dump(vault).data

        return jsonify({'vault': output})

    @use_kwargs({'title': fields.Str(),
                 'description': fields.Str()})
    @doc(description='Creates new vault, <id> - user prop')
    def post(self, id: int, **kwargs):
        """Creates Vault"""
        return VaultService.create(data=kwargs, id=id)

    @use_kwargs({'title': fields.Str(),
                 'description': fields.Str()})
    @doc(description='Updates vault, <id> - vault prop')
    def patch(self, id: int, **kwargs):
        """Updates Vault"""
        return VaultService.update(data=kwargs, id=id)

    @doc(description='Deletes vault, <id> - vault prop ')
    def delete(self, id: int):
        """Delete Vault"""
        return VaultService.delete(id=id)
