from app.api.service import VaultService
from app.api.serializers import VaultSchema
from app.models.models import Vault
from flask import request, jsonify

from flask_classful import FlaskView, route

from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc

from flask_sqlalchemy import BaseQuery


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

    @doc(description='Creates new vault, <id> - user prop')
    def post(self, id: int):
        """Create User"""
        data = request.get_json()
        return VaultService.create(data=data, id=id)

    @doc(description='Updates vault, <id> - vault prop')
    def patch(self, id: int):
        """Update user"""
        data = request.get_json()
        return VaultService.update(data=data, id=id)

    @doc(description='Deletes vault, <id> - vault prop ')
    def delete(self, id: int):
        """Delete User"""
        return VaultService.delete(id=id)
