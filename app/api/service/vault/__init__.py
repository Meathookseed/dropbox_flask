from app.api.decorators.token import token_required
from app.models.models import Vault, User
from app.shortcuts import dbsession

from flask import make_response, Response
from sqlalchemy.orm import Query


class VaultService:

    @staticmethod
    @token_required
    def list(current_user: User, **kwargs) -> Query:

        if not current_user.id == int(kwargs['id']):
            return make_response('Forbidden', 403)

        vaults = Vault.query.filter_by(owner_id=current_user.id)
        return vaults

    @staticmethod
    @token_required
    def one(current_user: User, **kwargs) -> Query:

        vault = Vault.query.filter_by(vault_id=int(kwargs['id'])).first()

        if vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        return vault

    @staticmethod
    @token_required
    def create(current_user: User, **kwargs) -> Response:

        if not current_user.id == int(kwargs['id']):
            return make_response('Forbidden', 403)

        data = kwargs['data']

        if not data:
            return make_response('No content', 204)

        new_vault = Vault(description=data['description'],
                          title=data['title'],
                          owner_id=current_user.id)

        dbsession.add(new_vault)
        dbsession.commit()

        return make_response('Created', 200)

    @staticmethod
    @token_required
    def update(current_user: User, **kwargs) -> Response:

        vault = Vault.query.filter_by(vault_id=kwargs['id']).first()

        if not vault or vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        data = kwargs['data']

        if 'description' in data:
            vault.description = data['description']

        if 'title' in data:
            vault.title = data['title']

        dbsession.commit()

        return make_response('Updated', 200)

    @staticmethod
    @token_required
    def delete(current_user: User, **kwargs) -> Response:

        vault = Vault.query.filter_by(vault_id=kwargs['id']).first()

        if not vault or vault not in current_user.vaults:
            return make_response('Forbidden', 403)

        dbsession.delete(vault)
        dbsession.commit()

        return make_response('Deleted', 200)
