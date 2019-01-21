from app.api.service import PhotoService
from flask import request

from flask_classful import FlaskView

from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc


class PhotoView(FlaskView, metaclass=ResourceMeta):

    @doc(description='handle photo update of user')
    def put(self, id: int):

        photo = request.files['photo']

        return PhotoService.create(id=id, photo=photo)
