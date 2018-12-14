from flask_classy import FlaskView
from flask_apispec.annotations import doc
from app.api.service.photo import PhotoService
from flask import request


class PhotoView(FlaskView):

    @doc(description='handle photo update of user')
    def put(self, id_):

        photo = request.files['file']

        return PhotoService.create(id_=id_, photo=photo)
