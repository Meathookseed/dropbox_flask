from app.api.decorators.token import token_required
from app.models.models import User
from app.shortcuts import dbsession

from flask import jsonify, current_app, Response, Request

import os

from werkzeug.utils import secure_filename


class PhotoService:

    @staticmethod
    @token_required
    def create(current_user: User, photo: Request, id: int) -> Response:

        try:

            if not current_user.id == id:
                return jsonify({"message": "permission denied"})

        except AttributeError:

            return jsonify({'error': 'not logged in'})

        filename = secure_filename(photo.filename)

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        user = User.query.filter_by(id=id).first()

        user.photo = file_folder

        dbsession.commit()

        return jsonify({'message': 'photo uploaded'})
