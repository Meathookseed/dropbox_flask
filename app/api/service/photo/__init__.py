from app.api.decorators.token import token_required
from app.models.models import User
from app.shortcuts import dbsession

from flask import current_app, make_response, Response

import os

from werkzeug.utils import secure_filename
from werkzeug.local import LocalProxy


class PhotoService:

    @staticmethod
    @token_required
    def create(current_user: User, photo: LocalProxy, id: int) -> Response:

        if not current_user.id == id:
            return make_response('Forbidden', 403)

        filename = secure_filename(photo.filename)

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        user = User.query.filter_by(id=id).first()

        user.photo = file_folder

        dbsession.commit()

        return make_response('Updated', 200)
