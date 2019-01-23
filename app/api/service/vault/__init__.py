from sqlalchemy.orm import Query

from app.api.decorators.token import token_required
from app.models.models import User, Vault
from app.shortcuts import dbsession


class VaultService:

    @staticmethod
    @token_required
    def list(current_user: User, **kwargs) -> Query or bool:

        if not current_user.id == int(kwargs['id']):
            return False

        vaults = Vault.query.filter_by(owner_id=current_user.id)

        return vaults

    @staticmethod
    @token_required
    def one(current_user: User, **kwargs) -> Query or bool:

        vault = Vault.query.filter_by(vault_id=int(kwargs['id'])).first()

        if vault not in current_user.vaults:
            return False

        return vault

    @staticmethod
    @token_required
    def create(current_user: User, **kwargs) -> bool or str:

        if not current_user.id == int(kwargs['id']):
            return False

        if bool(kwargs['data']) is False:
            return 'No data'

        data = kwargs['data']

        new_vault = Vault(description=data['description'],
                          title=data['title'],
                          owner_id=current_user.id)

        dbsession.add(new_vault)
        dbsession.commit()

        return True

    @staticmethod
    @token_required
    def update(current_user: User, **kwargs) -> bool or str:

        vault = Vault.query.filter_by(vault_id=kwargs['id']).first()

        if not vault or vault not in current_user.vaults:
            return False

        if bool(kwargs['data']) is False:
            return 'No data'

        data = kwargs['data']

        if 'description' in data:
            vault.description = data['description']

        if 'title' in data:
            vault.title = data['title']

        dbsession.commit()

        return True

    @staticmethod
    @token_required
    def delete(current_user: User, **kwargs) -> bool:

        vault = Vault.query.filter_by(vault_id=kwargs['id']).first()

        if not vault or vault not in current_user.vaults:
            return False

        dbsession.delete(vault)
        dbsession.commit()

        return True
