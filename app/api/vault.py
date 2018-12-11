from flask_classy import FlaskView, route

from app.api.service.vault import VaultService
from app.api.serializers.vault import VaultSchema

from flask import request

from flask_apispec.annotations import marshal_with, doc


class VaultView(FlaskView):

    @route('user_<public_id>')
    @marshal_with(VaultSchema(many=True))
    @doc(description='Get List of all users vaults, <public_id> - user prop')
    def index(self, public_id):
        """List of users"""
        return VaultService.list(public_id=public_id)

    @marshal_with(VaultSchema())
    @doc(description='Retrieve one vault, <id_> - vault prop')
    def get(self, id_):
        """Retrieve one user"""
        return VaultService.one(id_=id_)

    @doc(description='Creates new vault, <public_id> - user prop')
    def post(self, public_id):
        """Create User"""
        data = request.get_json()
        return VaultService.create(data=data, public_id=public_id)

    @doc(description='Updates vault, <id_> - vault prop')
    @marshal_with(VaultSchema())
    def patch(self, id_):
        """Update user"""
        data = request.get_json()
        return VaultService.update(data, id_=id_)

    @doc(description='Deletes vault, <id_> - vault prop ')
    def delete(self, id_):
        """Delete User"""
        return VaultService.delete(id_)
