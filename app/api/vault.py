from flask import jsonify,request
from app import db
from app.api import bp
from app.models import Vault
from app.api.utils.token import token_required


@bp.route('/user/<public_id>/vault/create', methods=['POST'])
@token_required
def vault_create(current_user, public_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'you have no permission'})

    data = request.get_json()

    new_vault = Vault(owner_id=current_user.id, description=data['description'], title=data['title'])

    db.session.add(new_vault)
    db.session.commit()

    return jsonify({'message': 'New vault created'})


@bp.route('/vault', methods=['GET'])
@token_required
def vault_list(current_user):

    if not current_user.admin:
        return jsonify({'message': 'you have no permission'})

    vaults = Vault.query.all()
    output = []
    for vault in vaults:
        vault_data = dict()
        vault_data['title'] = vault.title
        vault_data['description'] = vault.description
        vault_data['vault_id'] = vault.vault_id
        vault_data['owner_id'] = vault.owner_id
        output.append(vault_data)

    return jsonify({'vaults': output})


@bp.route('/user/<public_id>/vault/<vault_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def vault_ud(current_user, public_id, vault_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    if request.method == 'GET':

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if not vault:
            return jsonify({'message': 'No vault like this'})

        output = []
        vault_data = dict()
        vault_data['title'] = vault.title
        vault_data['description'] = vault.description
        vault_data['vault_id'] = vault.vault_id
        vault_data['owner_id'] = vault.owner_id
        output.append(vault_data)

        return jsonify({'vault': output})

    if request.method == 'PUT':

        data = request.get_json()

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if not vault:
            return jsonify({'message': 'There is no vault'})

        if 'title' in data:
            vault.title = data['title']

        if 'description' in data:
            vault.description = data['description']

        vault.owner_id = current_user.id
        db.session.commit()

        return jsonify({'message': 'vault was updated'})

    if request.method == 'DELETE':

        if not current_user.public_id == public_id:
            return jsonify({'message': 'permission denied'})

        vault = Vault.query.filter_by(vault_id=vault_id).first()

        if not vault:
            return jsonify({'message': 'there is no vault like this'})

        db.session.delete(vault)
        db.session.commit()

        return jsonify({"message": "vault was deleted"})
