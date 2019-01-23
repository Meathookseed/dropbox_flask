import os

from flask import current_app
from werkzeug.utils import secure_filename

from app.api.decorators.token import token_required
from app.models.models import User
from app.shortcuts import dbsession


class PhotoService:

    @staticmethod
    @token_required
    def create(current_user: User, **kwargs) -> bool or str:

        if not current_user.id == kwargs['id']:
            return False

        if bool(kwargs['photo']) is False:
            return 'No data'

        photo = kwargs['photo']

        filename = secure_filename(photo.filename)

        file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        photo.save(file_folder)

        user = User.query.filter_by(id=kwargs['id']).first()

        user.photo = file_folder

        dbsession.commit()

        return True
