import os

from app.api.decorators.token import token_required
from app.models.models import File, User, Vault
from app.shortcuts import dbsession


class FileService:

    @staticmethod
    @token_required
    def list(current_user: User, **kwargs)-> bool:

        files = File.query.filter_by(vault_id=kwargs['vault_id'])

        vault = Vault.query.filter_by(vault_id=kwargs['vault_id']).first()

        if current_user is None or current_user is None or vault not in current_user.vaults:
            return False

        return files

    @staticmethod
    @token_required
    def one(current_user: User, **kwargs) -> bool:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if current_user is None or file not in current_user.files:
            return False

        return file

    @staticmethod
    @token_required
    def create(current_user: User, **kwargs) -> bool or str or dict:

        vault = Vault.query.filter_by(vault_id=kwargs['vault_id']).first()

        if current_user is None or  vault not in current_user.vaults:
            return False

        if bool(kwargs['data']) is False:
            return 'No data'

        data = kwargs['data']

        new_file = File(name=data['name'],
                        description=data['description'],
                        vault_id=kwargs['vault_id'],
                        owner_id=vault.owner_id)

        dbsession.add(new_file)

        dbsession.commit()

        return new_file.file_id

    @staticmethod
    @token_required
    def update(current_user: User, **kwargs) -> bool or str:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if current_user is None or not file or not current_user.id == file.owner_id:
            return False

        if bool(kwargs['data']) is False:
            return 'No data'

        data = kwargs['data']

        if 'description' in data:
            file.description = data['description']

        if 'name' in data:
            file.name = data['name']

        dbsession.commit()

        return True

    @staticmethod
    @token_required
    def delete(current_user: User, **kwargs) -> bool:

        file = File.query.filter_by(file_id=kwargs['id']).first()

        if current_user is None or not file or not current_user.id == file.owner_id:
            return False

        dbsession.delete(file)
        dbsession.commit()

        if file.data:
            os.remove(file.data)

        return True
