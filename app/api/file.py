from flask_classful import FlaskView, route
from app.models.models import File
from app.api.service import FileService
from app.api.serializers import FileSchema

from flask import request, jsonify

from flask_apispec import ResourceMeta
from flask_apispec.annotations import marshal_with, doc, use_kwargs

from flask_sqlalchemy import BaseQuery

from marshmallow import fields


class FileView(FlaskView, metaclass=ResourceMeta):

    @route('vault_<vault_id>/',)
    @marshal_with(FileSchema(many=True))
    @doc(description='Get List of all files, <vault_id> - vault prop')
    def index(self, vault_id: int):
        """List of files"""
        response = FileService.list(vault_id=vault_id)

        if not isinstance(response, BaseQuery):
            return response

        file_schema = FileSchema(many=True)

        output = file_schema.dump(response).data

        return jsonify({'files': output})

    @marshal_with(FileSchema())
    @doc(description='Retrieve one file, <id> - file prop')
    def get(self, id: int):
        """Retrieve one user"""

        file = FileService.one(id=id)

        if not isinstance(file, File):
            return file

        file_schema = FileSchema()

        output = file_schema.dump(file).data

        return jsonify({'user': output})

    @use_kwargs({'name': fields.Str(),
                 "description": fields.Str()})
    @doc(description='Creates new file, <vault_id> - vault prop')
    def post(self, vault_id: int, **kwargs):
        """Create User"""
        return FileService.create(vault_id=vault_id, data=kwargs)

    @use_kwargs({'name': fields.Str(),
                 "description": fields.Str()})
    @doc(description='Updates file, <id> - file prop')
    def patch(self, id: int, **kwargs):
        """Update user"""
        return FileService.update(data=kwargs, id=id)

    @doc(description='Deletes file, <id> - file prop ')
    def delete(self, id: int):
        """Delete User"""
        return FileService.delete(id=id)
