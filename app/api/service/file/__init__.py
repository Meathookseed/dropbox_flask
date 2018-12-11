from flask import jsonify
from app.models.models import File, Vault
from app.shortcuts import dbsession
from app.api.decorators.token import token_required
from app.api.serializers.file import FileSchema


class FileService:

    @staticmethod
    @token_required
    def list(current_user, vault_id):

        files = File.query.filter_by(vault_id=vault_id)

        if files not in current_user.files:
            return jsonify({'message': 'permission denied'})

        if not files:
            return jsonify({'message': 'no files in vault'})

        file_schema = FileSchema(many=True)

        output = file_schema.dump(files).data

        return jsonify({'files': output})

    @staticmethod
    @token_required
    def one(current_user, id_):

        file = File.query.filter_by(file_id=id_).first()

        if file not in current_user.files:
            return jsonify({'message': 'permission denied'})

        if not file:
            return jsonify({'message': 'no such file'})

        file_schema = FileSchema()

        output = file_schema.dump(file).data

        return jsonify({'user': output})

    @staticmethod
    @token_required
    def create(current_user, vault_id, data):

        vault = Vault.query.filter_by(vault_id=vault_id)

        if vault not in current_user.vaults:
            return jsonify({"message": "permission denied"})

        if not vault:
            return jsonify({'message': 'no such vault'})

        new_file = File(name=data['name'], description=data['description'], vault_id=vault_id)

        dbsession.add(new_file)
        dbsession.commit()

        return jsonify({'message': 'file created'})

    @staticmethod
    @token_required
    def update(current_user, data, id_):

        file = File.query.filter_by(id=id_).first()

        if not current_user.id == file.owner_id:
            return jsonify({"message": "permission denied"})

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        dbsession.commit(file)

        return jsonify({"message": "file updated"})

    @staticmethod
    @token_required
    def delete(current_user, id_):

        file = File.query.filter_by(id=id_).fiirst()

        if not current_user.id == file.owner_id:
            return jsonify({"message": "permission denied"})

        dbsession.delete(file)

        return jsonify({'message': 'file has been deleted'})
