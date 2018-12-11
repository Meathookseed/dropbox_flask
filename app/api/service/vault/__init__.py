from app.models.models import Vault
from flask import jsonify
from app.shortcuts import dbsession
from app.api.decorators.token import token_required
from app.api.serializers.vault import VaultSchema


class VaultService:

    @staticmethod
    @token_required
    def list(current_user, id_):

        if not current_user.id == id_:
            return jsonify({'message': 'permission denied'})

        vaults = Vault.query.filter_by(owner_id=id_)
        schema = VaultSchema(many=True)
        output = schema.dump(vaults).data

        return jsonify({'vaults': output})

    @staticmethod
    @token_required
    def one(current_user, id_):

        if not current_user.id == id_ and not current_user.admin:
            return jsonify({'message': 'permission denied'})

        vault = Vault.query.filter_by(vault_id=id_).first()

        if not vault:
            return jsonify({"message": 'no vault'})
        schema = VaultSchema()

        output = schema.dump(vault).data

        return jsonify({'vault': output})

    @staticmethod
    @token_required
    def create(current_user, id_, data):

        if not current_user.id == id_:
            return jsonify({'message': 'permission denied'})

        new_vault = Vault(description=data['description'], title=data['title'], owner_id=current_user.id)

        dbsession.add(new_vault)
        dbsession.commit()

        return jsonify({'message': 'vault created'})

    @staticmethod
    @token_required
    def update(data, current_user, public_id, id_):

        if not current_user.public_id == public_id:
            return jsonify({'message': 'permission denied'})

        vault = Vault.query.filter_by(id=id_).first()

        if 'description' in data:
            vault.description = data['description']

        if 'title' in data:
            vault.title = data['title']

        dbsession.commit(vault)

        return jsonify({'message': 'vault updated'})

    @staticmethod
    @token_required
    def delete(current_user, public_id, id_):

        if not current_user.public_id == public_id:
            return jsonify({'message': 'permission denied'})

        vault = Vault.query.filter_by(id=id_).first()

        dbsession.delete(vault)

        return jsonify({'message': 'vault has been deleted'})
