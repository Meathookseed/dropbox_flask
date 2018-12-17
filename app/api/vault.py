from app.api.service.vault import VaultService
from app.api.serializers.vault import VaultSchema

from flask import request

from flask_classy import FlaskView, route

from flask_apispec.annotations import marshal_with, doc


class VaultView(FlaskView):

    @route('user_<id>')
    @marshal_with(VaultSchema(many=True))
    @doc(description='Get List of all users vaults, <id> - user prop')
    def index(self, id):
        """List of users"""
        return VaultService.list(id=id)

    @marshal_with(VaultSchema)
    @doc(description='Retrieve one vault, <id> - vault prop')
    def get(self, id):
        """Retrieve one user"""
        return VaultService.one(id=id)

    @doc(description='Creates new vault, <public_id> - user prop')
    def post(self, public_id):
        """Create User"""
        data = request.get_json()
        return VaultService.create(data=data, public_id=public_id)

    @doc(description='Updates vault, <id> - vault prop')
    @marshal_with(VaultSchema)
    def patch(self, id):
        """Update user"""
        data = request.get_json()
        return VaultService.update(data, id=id)

    @doc(description='Deletes vault, <id> - vault prop ')
    def delete(self, id):
        """Delete User"""
        return VaultService.delete(id)
