from flask_classy import FlaskView, route

from app.api.service.file import FileService
from app.api.serializers.file import FileSchema

from flask import request

from flask_apispec.annotations import marshal_with, doc


class FileView(FlaskView):

    @route('vault_<vault_id>',)
    @marshal_with(FileSchema(many=True))
    @doc(description='Get List of all files, <vault_id> - vault prop')
    def index(self, vault_id):
        """List of files"""
        return FileService.list(vault_id=vault_id)

    @marshal_with(FileSchema)
    @doc(description='Retrieve one file, <id> - file prop')
    def get(self, id):
        """Retrieve one user"""
        return FileService.one(id=id)

    @doc(description='Creates new file, <vault_id> - vault prop')
    def post(self, vault_id):
        """Create User"""
        data = request.get_json()
        return FileService.create(data=data, vault_id=vault_id)

    @doc(description='Updates file, <id> - file prop')
    @marshal_with(FileSchema)
    def patch(self, id):
        """Update user"""
        data = request.get_json()
        return FileService.update(data=data, id=id)

    @doc(description='Deletes file, <id> - file prop ')
    def delete(self, id):
        """Delete User"""
        return FileService.delete(id=id)
