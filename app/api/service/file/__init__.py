from app.api.decorators.token import token_required
from app.models.models import File, Vault, User
from app.shortcuts import dbsession
from flask import jsonify
from sqlalchemy.orm import Query
from werkzeug.local import LocalProxy
import os


class FileService:

    @staticmethod
    @token_required
    def list(current_user: User, vault_id: int)-> Query:

        files = File.query.filter_by(vault_id=vault_id)

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if vault not in current_user.vaults:
            return jsonify({'message': 'permission denied'})

        for file in files:
            if not file:
                return jsonify({'message': 'no files in vault'})

        return files

    @staticmethod
    @token_required
    def one(current_user: User, id: int) -> Query:

        file = File.query.filter_by(file_id=id).first()

        if not file:
            return jsonify({'message': 'no such file'})

        if file not in current_user.files:
            return jsonify({'message': 'permission denied'})
        return file

    @staticmethod
    @token_required
    def create(current_user: User, vault_id: int, data: dict) -> LocalProxy:

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if not vault:
            return jsonify({'message': 'no such vault'})

        if vault not in current_user.vaults:
            return jsonify({"message": "permission denied"})

        new_file = File(name=data['name'],
                        description=data['description'],
                        vault_id=vault_id,
                        owner_id=vault.owner_id)

        dbsession.add(new_file)

        dbsession.commit()

        return jsonify({"file_id": new_file.file_id})

    @staticmethod
    @token_required
    def update(current_user: User, data: dict, id: int) -> LocalProxy:

        file = File.query.filter_by(file_id=id).first()

        if not current_user.id == file.owner_id:
            return jsonify({"message": "permission denied"})

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        dbsession.commit()

        return jsonify({"message": "file updated"})

    @staticmethod
    @token_required
    def delete(current_user: User, id: int) -> LocalProxy:

        file = File.query.filter_by(file_id=id).first()

        if not current_user.id == file.owner_id:
            return jsonify({"message": "permission denied"})

        dbsession.delete(file)
        dbsession.commit()

        if file.data:
            os.remove(file.data)

        return jsonify({'message': 'file has been deleted'})
