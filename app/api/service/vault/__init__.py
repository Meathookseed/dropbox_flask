from app import db
from app.api.models.vault import Vault
from flask import jsonify

class VaultService:

    @staticmethod
    def list(id_):

        vaults = Vault.query.filter_by(owner_id=id_)

        return vaults


    @staticmethod
    def create(data):

        new_vault = Vault(description=data['description'], title=data['title'])

        db.session.add(new_vault)
        db.session.commit()

        return new_vault

    @staticmethod
    def update(data, id_):

        vault = Vault.query.filter_by(id=id_).first()

        if 'description' in data:
            vault.description = data['description']

        if 'title' in data:
            vault.title = data['title']

        db.session.commit(vault)

        return vault

    @staticmethod
    def delete(id_):

        vault = Vault.query.filter_by(id=id_).fiirst()

        db.session.delete(vault)

        return jsonify({'message': 'vault has been deleted'})

