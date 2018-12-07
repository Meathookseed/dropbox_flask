from app import db
from flask import jsonify
from app.api.models.file import File


class FileService:

    @staticmethod
    def list(id_):

        files = File.query.filter_by(owner_id=id_)

        return files

    @staticmethod
    def create(data):

        new_file = File(name=data['name'], description=data['description'])

        db.session.add(new_file)
        db.session.commit()

        return new_file

    @staticmethod
    def update(data, id_):

        file = File.query.filter_by(id=id_).first()

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        db.session.commit(file)

        return file

    @staticmethod
    def delete(id_):

        file = File.query.filter_by(id=id_).fiirst()

        db.session.delete(file)

        return jsonify({'message': 'file has been deleted'})
