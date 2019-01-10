from app.api.service.photo import PhotoService

from flask import request

from flask_classy import FlaskView

from flask_apispec.annotations import doc


class PhotoView(FlaskView):

    @doc(description='handle photo update of user')
    def put(self, id: int):

        photo = request.files['photo']

        return PhotoService.create(id=id, photo=photo)
