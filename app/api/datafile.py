from flask import request
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc
from flask_classful import FlaskView

from app.openapi_doc_parameters import DOCS_PARAMS_FOR_FILE
from app.api.service import DataFileService


@doc(tags=['File'])
class DataView(FlaskView, metaclass=ResourceMeta):

    @doc(description='handle photo update of user',
         consumes=['multipart/form-data'],
         params=DOCS_PARAMS_FOR_FILE)
    def put(self, id: int):
        datafile = request.files['file']
        return DataFileService.create(id=id, datafile=datafile)
