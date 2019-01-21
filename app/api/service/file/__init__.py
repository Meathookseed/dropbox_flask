from app.api.decorators.token import token_required
from app.models.models import File, Vault, User
from app.shortcuts import dbsession
from flask import jsonify, make_response, Response
from sqlalchemy.orm import Query
import os


class FileService:

    @staticmethod
    @token_required
    def list(current_user: User, **kwargs)-> Query:

        files = File.query.filter_by(vault_id=kwargs['vault_id'])

        vault = Vault.query.filter_by(vault_id=kwargs['vault_id']).first()

        if vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        return files

    @staticmethod
    @token_required
    def one(current_user: User, **kwargs) -> Query:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if file not in current_user.files:
            return make_response('Forbidden', 403)

        return file

    @staticmethod
    @token_required
    def create(current_user: User, **kwargs) -> Response:

        vault = Vault.query.filter_by(vault_id=kwargs['vault_id']).first()

        if vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        data = kwargs['data']

        new_file = File(name=data['name'],
                        description=data['description'],
                        vault_id=kwargs['vault_id'],
                        owner_id=vault.owner_id)

        dbsession.add(new_file)

        dbsession.commit()

        return jsonify({"file_id": new_file.file_id})

    @staticmethod
    @token_required
    def update(current_user: User, **kwargs) -> Response:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if not file or not current_user.id == file.owner_id:
            return make_response('Forbidden', 403)

        data = kwargs['data']

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        dbsession.commit()

        return make_response('Updated', 200)

    @staticmethod
    @token_required
    def delete(current_user: User, **kwargs) -> Response:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if not file or not current_user.id == file.owner_id:
            return make_response('Forbidden', 403)

        dbsession.delete(file)
        dbsession.commit()

        if file.data:
            os.remove(file.data)

        return make_response('Deleted', 200)
