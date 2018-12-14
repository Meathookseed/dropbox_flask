from app.api.serializers.photo import PhotoSerializer
from app.models.models import User
from flask import jsonify, current_app
from werkzeug.utils import secure_filename
from app.shortcuts import dbsession
import os
from app.api.decorators.token import token_required

class PhotoService:

    @staticmethod
    @token_required
    def create(current_user, photo, id_):

        try:

            if not current_user.id == id_:
                return jsonify({"message": "permission denied"})

        except AttributeError:

            return jsonify({'error': 'not logged in'})

        filename = secure_filename(photo.filename)

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        user = User.query.filter_by(id=id_).first()

        user.photo = file_folder

        print(user.photo)

        dbsession.commit()

        return jsonify({'message':'photo uploaded'})
