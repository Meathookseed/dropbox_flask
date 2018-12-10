from app.models.models import Vault
from flask import jsonify
from app.shortcuts import dbsession


class VaultService:

    @staticmethod
    def list(id_):

        vaults = Vault.query.filter_by(owner_id=id_)

        return vaults


    @staticmethod
    def create(data):

        new_vault = Vault(description=data['description'], title=data['title'])

        dbsession.add(new_vault)
        dbsession.commit()

        return new_vault

    @staticmethod
    def update(data, id_):

        vault = Vault.query.filter_by(id=id_).first()

        if 'description' in data:
            vault.description = data['description']

        if 'title' in data:
            vault.title = data['title']

        dbsession.commit(vault)

        return vault

    @staticmethod
    def delete(id_):

        vault = Vault.query.filter_by(id=id_).fiirst()

        dbsession.delete(vault)

        return jsonify({'message': 'vault has been deleted'})

