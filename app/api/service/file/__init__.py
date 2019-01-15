from app.api.decorators.token import token_required
from app.models.models import File, Vault, User
from app.shortcuts import dbsession
from flask import jsonify, make_response, Response
from sqlalchemy.orm import Query
import os


class FileService:

    @staticmethod
    @token_required
    def list(current_user: User, vault_id: int)-> Query:

        files = File.query.filter_by(vault_id=vault_id)

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        for file in files:
            if not file:
                return make_response('No content', 204)

        return files

    @staticmethod
    @token_required
    def one(current_user: User, id: int) -> Query:

        file = File.query.filter_by(file_id=id).first()

        if not file:
            return make_response('No content', 204)

        if file not in current_user.files:
            return make_response('Forbidden', 403)
        return file

    @staticmethod
    @token_required
    def create(current_user: User, vault_id: int, data: dict) -> Response:

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if not vault:
            return make_response('No content', 204)

        if vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        new_file = File(name=data['name'],
                        description=data['description'],
                        vault_id=vault_id,
                        owner_id=vault.owner_id)

        dbsession.add(new_file)

        dbsession.commit()

        return jsonify({"file_id": new_file.file_id})

    @staticmethod
    @token_required
    def update(current_user: User, data: dict, id: int) -> Response:

        file = File.query.filter_by(file_id=id).first()

        if not current_user.id == file.owner_id:
            return make_response('Forbidden', 403)

        if not data:
            return make_response('No content', 204)

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        dbsession.commit()

        return make_response('Updated', 200)

    @staticmethod
    @token_required
    def delete(current_user: User, id: int) -> Response:

        file = File.query.filter_by(file_id=id).first()

        if not current_user.id == file.owner_id:
            return make_response('Forbidden', 403)

        if not file:
            return make_response('No content', 204)

        dbsession.delete(file)
        dbsession.commit()

        if file.data:
            os.remove(file.data)

        return make_response('Deleted', 200)
