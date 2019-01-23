import os

from flask import Response, current_app, jsonify, make_response
from werkzeug.utils import secure_filename

from app.api.decorators.token import token_required
from app.models.models import File, User
from app.shortcuts import dbsession


class DataFileService:

    @staticmethod
    @token_required
    def create(current_user: User, **kwargs) -> Response:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if not file:
            file.data = None

        datafile = kwargs['datafile']

        filename = secure_filename(datafile.filename)

        if not current_user.id == file.owner_id:
            return make_response('Permission denied', 401)

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username, filename)

        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)):
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username))

        datafile.save(file_folder)

        file.data = file_folder
        dbsession.commit()

        return jsonify({'message': 'photo uploaded'})
