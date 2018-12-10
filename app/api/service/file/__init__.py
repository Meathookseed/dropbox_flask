from flask import jsonify
from app.models.models import File
from app.shortcuts import dbsession


class FileService:

    @staticmethod
    def list(id_):

        files = File.query.filter_by(owner_id=id_)

        return files

    @staticmethod
    def create(data):

        new_file = File(name=data['name'], description=data['description'])

        dbsession.add(new_file)
        dbsession.commit()

        return new_file

    @staticmethod
    def update(data, id_):

        file = File.query.filter_by(id=id_).first()

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        dbsession.commit(file)

        return file

    @staticmethod
    def delete(id_):

        file = File.query.filter_by(id=id_).fiirst()

        dbsession.delete(file)

        return jsonify({'message': 'file has been deleted'})
