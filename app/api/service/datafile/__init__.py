from app.shortcuts import dbsession
from app.api.decorators.token import token_required
from app.models.models import File

from flask import jsonify, current_app

import os

from werkzeug.utils import secure_filename


class DataFileService:

    @staticmethod
    @token_required
    def create(current_user, datafile, id):

        filename = secure_filename(datafile.filename)

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(file_folder)

        datafile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        file = File.query.filter_by(file_id=id).first()

        if not file:
            return jsonify({'message': "no file"})
        try:
            if not current_user.id == file.owner_id:
                return jsonify({"message": "permission denied"})

        except AttributeError:

            return jsonify({'error': 'not logged in'})

        file.data = file_folder
        print(file.data)
        dbsession.commit()

        return jsonify({'message': 'photo uploaded'})
