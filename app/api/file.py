from flask import request, jsonify
from app import db
from app.api.models.models import File, Vault
from app.api.decorators.token import token_required
from app.api import bp


@bp.route('/user/<public_id>/file/create', methods=['POST'])
@token_required
def file_create(current_user, public_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    data = request.get_json()

    vault = Vault.query.filter_by(owner_id=current_user.id).first()

    new_file = File(name=data['name'], description=data['description'], owner_id=current_user.id,
                    vault_id=vault.vault_id)

    db.session.add(new_file)

    db.session.commit()

    return jsonify({'message': 'File Created!'})


@bp.route('/user/<public_id>/vault/<vault_id>/file', methods=['POST'])
@token_required
def file_list(current_user, public_id, vault_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    vault = Vault.query.filter_by(vault_id=vault_id).first()
    files = File.query.filter_by(owner_id=current_user.id)

    output = []

    for file in files:
        file_data = dict()
        file_data['name'] = file.name
        file_data['description'] = file.description
        file_data['vault_id'] = vault.vault_id
        file_data['owner_id'] = file.owner_id
        file_data['data'] = file.data
        output.append(file_data)

    return jsonify({'Files': output})


@bp.route('/user/<public_id>/file/<file_id>', methods=['PUT', "DELETE"])
@token_required
def file_update(current_user, public_id, file_id):

    data = request.get_json()

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    if request.method == 'PUT':

        file = File.query.filter_by(file_id=file_id).first()

        if not file:
            return jsonify({'message': 'there is no such file'})

        if 'name' in data:
            file.name = data['name']

        if 'description' in data:
            file.description = data['description']

        db.session.commit()

        return jsonify({"message": "file updated"})

    if request.method == 'DELETE':

        file = File.query.filter_by(file_id=file_id).first()

        if not file:
            return jsonify({'message': 'there is no file like this'})

        db.session.delete(file)
        db.session.commit()

        return jsonify({"message": "file was deleted"})


