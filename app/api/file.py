from flask_classy import FlaskView, route

from app.api.service.file import FileService
from app.api.serializers.file import FileSchema

from flask import request, jsonify

from flask_apispec.annotations import marshal_with, doc


class FileView(FlaskView):

    @route('vault_<vault_id>',)
    @marshal_with(FileSchema(many=True))
    @doc(description='Get List of all files, <vault_id> - vault prop')
    def index(self, vault_id):
        """List of files"""
        files = FileService.list(vault_id=vault_id)

        file_schema = FileSchema(many=True)

        output = file_schema.dump(files).data

        return jsonify({'files': output})

    @marshal_with(FileSchema)
    @doc(description='Retrieve one file, <id> - file prop')
    def get(self, id):
        """Retrieve one user"""
        file = FileService.one(id=id)

        file_schema = FileSchema()

        output = file_schema.dump(file).data

        return jsonify({'user': output})

    @doc(description='Creates new file, <vault_id> - vault prop')
    def post(self, vault_id):
        """Create User"""

        data = request.get_json()
        return FileService.create(data=data, vault_id=vault_id)

    @doc(description='Updates file, <id> - file prop')
    def patch(self, id):
        """Update user"""
        data = request.get_json()
        return FileService.update(data=data, id=id)

    @doc(description='Deletes file, <id> - file prop ')
    def delete(self, id):
        """Delete User"""
        return FileService.delete(id=id)
