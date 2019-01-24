from flask import jsonify, make_response
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, marshal_with, use_kwargs
from flask_classful import FlaskView, route
from marshmallow import fields

from app.api.serializers import FileSchema
from app.api.service import FileService
from app.openapi_doc_parameters import *


@doc(tags=['File'])
class FileView(FlaskView, metaclass=ResourceMeta):

    @route('vault_<vault_id>/',)
    @marshal_with(FileSchema(), code='200')
    @doc(description='Get List of all files, vault_id - file prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=GET_CODES)
    def index(self, vault_id: int):
        """List of files"""

        result = FileService.list(vault_id=vault_id)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'files': FileSchema(many=True).dump(result).data})

    @marshal_with(FileSchema(), code='200')
    @doc(description='Retrieve one file, id - file prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=GET_CODES)
    def get(self, id: int):
        """Retrieve one user"""

        result = FileService.one(id=id)

        if result is False:
            return make_response('No permission', 403)

        return jsonify({'user': FileSchema().dump(result).data})

    @use_kwargs({'name': fields.Str(),
                 "description": fields.Str()})
    @marshal_with(None)
    @doc(description='Creates new file, vault_id - file prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=POST_CODES)
    def post(self, vault_id: int, **kwargs):
        """Create User"""

        result = FileService.create(vault_id=vault_id, data=kwargs)

        if result is False:
            return make_response('No permission', 403)
        elif result == 'No data':
            return make_response('No data', 204)

        return jsonify({'file_id': result})

    @use_kwargs({'name': fields.Str(),
                 "description": fields.Str()})
    @marshal_with(None)
    @doc(description='Updates file, <id> - file prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=PATCH_CODES)
    def patch(self, id: int, **kwargs):
        """Update user"""

        result = FileService.update(data=kwargs, id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result == 'No data':
            return make_response('No data', 204)

        return make_response('Updated', 200)

    @marshal_with(None)
    @doc(description='Delete vault, id- vault prop',
         params=DOCS_PARAMS_FOR_TOKEN,
         responses=DELETE_CODES)
    def delete(self, id: int):
        """Delete User"""

        result = FileService.delete(id=id)

        if result is False:
            return make_response('No permission', 403)
        elif result is True:
            return make_response('Deleted', 200)
