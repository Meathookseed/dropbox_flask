from flask import request
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc
from flask_classful import FlaskView

from app.api.service import DataFileService


class DataView(FlaskView, metaclass=ResourceMeta):

    @doc(description='handle file update, <id> - file prop')
    def put(self, id: int):
        datafile = request.files['file']
        return DataFileService.create(id=id, datafile=datafile)
