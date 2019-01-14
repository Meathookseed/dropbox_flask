from app.api.decorators.token import token_required
from app.models.models import Vault, User
from app.shortcuts import dbsession

from flask import jsonify, Response
from sqlalchemy.orm import Query


class VaultService:

    @staticmethod
    @token_required
    def list(current_user: User, id: int) -> Query:

        if not current_user.id == int(id):
            return jsonify({'message': 'permission denied'})

        vaults = Vault.query.filter_by(owner_id=current_user.id)

        if not vaults:
            return jsonify({'message': 'there is no vaults'})

        return vaults

    @staticmethod
    @token_required
    def one(current_user: User, id: int) -> Query:

        vault = Vault.query.filter_by(vault_id=int(id)).first()

        if vault not in current_user.vaults:
            return jsonify({'message': 'permission denied'})

        if not vault:
            return jsonify({"message": 'no vault'})

        return vault

    @staticmethod
    @token_required
    def create(current_user: User, data=None, id=0) -> Response:

        if not current_user.id == int(id):
            return jsonify({'message': 'permission denied'})

        if not data:
            return jsonify({'message': 'empty'})

        new_vault = Vault(description=data['description'],
                          title=data['title'],
                          owner_id=id)

        dbsession.add(new_vault)
        dbsession.commit()

        return jsonify({'message': 'vault created'})

    @staticmethod
    @token_required
    def update(data: dict, current_user: User, id: int) -> Response:

        vault = Vault.query.filter_by(id=id).first()

        if vault not in current_user.vaults:
            return jsonify({'message': 'permission denied'})

        if 'description' in data:
            vault.description = data['description']

        if 'title' in data:
            vault.title = data['title']

        dbsession.commit()

        return jsonify({'message': 'vault updated'})

    @staticmethod
    @token_required
    def delete(current_user: User, id: int) -> Response:

        vault = Vault.query.filter_by(vault_id=id).first()
        if vault not in current_user.vaults:
            return jsonify({'message': 'permission denied'})

        dbsession.delete(vault)
        dbsession.commit()

        return jsonify({'message': 'vault has been deleted'})
