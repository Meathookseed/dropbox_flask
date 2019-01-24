from flask import request, make_response
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc
from flask_classful import FlaskView

from app.openapi_doc_parameters import *
from app.api.service import PhotoService


@doc(tags=['User'])
class PhotoView(FlaskView, metaclass=ResourceMeta):

    @doc(description='Handle photo update of user',
         consumes=['multipart/form-data'],
         params=DOCS_PARAMS_FOR_PHOTO)
    def put(self, id: int):

        photo = request.files['photo']

        result = PhotoService.create(id=id, photo=photo)

        if result is False:
            return make_response('No permission', 403)
        elif result == 'No data':
            return make_response('No data', 204)
        elif result is True:
            return make_response('Uploaded', 200)
