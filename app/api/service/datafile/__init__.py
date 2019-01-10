from app.shortcuts import dbsession
from app.api.decorators.token import token_required
from app.models.models import File, User

from flask import jsonify, current_app

import os

from werkzeug.utils import secure_filename
from werkzeug.local import LocalProxy

class DataFileService:

    @staticmethod
    @token_required
    def create(current_user: User, datafile: LocalProxy , id: int) -> LocalProxy:

        file = File.query.filter_by(file_id=id).first()

        if not file:
            file.data = None

        filename = secure_filename(datafile.filename)

        if not current_user.id == file.owner_id:
            return jsonify({"message": "permission denied"})

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username, filename)

        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)):
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username))

        datafile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username, filename))
        print('created')
        file.data = file_folder
        dbsession.commit()

        return jsonify({'message': 'photo uploaded'})
