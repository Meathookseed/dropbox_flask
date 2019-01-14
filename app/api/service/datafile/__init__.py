from app.shortcuts import dbsession
from app.api.decorators.token import token_required
from app.models.models import File, User

from flask import jsonify, current_app, Response, Request
import os

from werkzeug.utils import secure_filename


class DataFileService:

    @staticmethod
    @token_required
    def create(current_user: User, datafile: Request, id: int) -> Response:

        file = File.query.filter_by(file_id=id).first()

        if not file:
            file.data = None
        print(datafile)
        filename = secure_filename(datafile.filename)

        if not current_user.id == file.owner_id:
            return jsonify({"message": "permission denied"})

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username, filename)

        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)):
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username))

        datafile.save(file_folder)
        print('created')
        file.data = file_folder
        dbsession.commit()

        return jsonify({'message': 'photo uploaded'})
