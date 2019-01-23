from flask import request
from flask_apispec import ResourceMeta
from flask_apispec.annotations import doc, use_kwargs
from flask_classful import FlaskView

from app.api.service import PhotoService


class PhotoView(FlaskView, metaclass=ResourceMeta):

    @use_kwargs()
    @doc(description='handle photo update of user')
    def put(self, id: int):

        photo = request.files['photo']

        return PhotoService.create(id=id, photo=photo)
