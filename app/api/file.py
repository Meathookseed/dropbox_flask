from flask_classy import FlaskView, route

from app.api.service.vault import VaultService
from app.api.serializers.vault import VaultSchema

from flask import request

from flask_apispec.annotations import marshal_with, doc


class FileView(FlaskView):

    @route('vault_<vault_id>')
    @marshal_with(VaultSchema(many=True))
    @doc(description='Get List of all files, <vault_id> - vault prop')
    def index(self, vault_id):
        """List of files"""
        return VaultService.list(vault_id=vault_id)

    @marshal_with(VaultSchema())
    @doc(description='Retrieve one file, <id_> - file prop')
    def get(self, id_):
        """Retrieve one user"""
        return VaultService.one(id_=id_)

    @doc(description='Creates new file, <vault_id> - vault prop')
    def post(self, vault_id):
        """Create User"""
        data = request.get_json()
        return VaultService.create(data=data, vault_id=vault_id)

    @doc(description='Updates file, <id_> - file prop')
    @marshal_with(VaultSchema())
    def patch(self, id_):
        """Update user"""
        data = request.get_json()
        return VaultService.update(data, id_=id_)

    @doc(description='Deletes file, <id_> - file prop ')
    def delete(self, id_):
        """Delete User"""
        return VaultService.delete(id_)
