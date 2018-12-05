from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from functools import wraps
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config['secret_key'] = 'thisissecret'

file_path = os.path.abspath(os.getcwd())+"/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    vaults = db.relationship('Vault')
    photo = db.Column(db.LargeBinary)
    admin = db.Column(db.Boolean)


class Vault(db.Model):
    vault_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String())
    files = db.relationship('File')


class File(db.Model):
    file_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vault_id = db.Column(db.Integer, db.ForeignKey('vault.vault_id'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String())
    data = db.Column(db.LargeBinary)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Bearer' in request.headers:
            token = request.headers['Bearer']

        if not token:
            return jsonify({'message': 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['secret_key'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except ValueError:
            return jsonify({'message': 'Token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/user", methods=['GET'])
@token_required
def user_list(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()
    output = []

    for user in users:
        user_data = dict()
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        user_data['password'] = user.password
        user_data['id'] = user.id
        output.append(user_data)

    return jsonify({'users': output})


@app.route("/user/<public_id>", methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin and not current_user.public_id == public_id:
        return jsonify({'message': 'You have no permission'})

    user = User.query.filter_by(public_id=public_id).first()

    if not User:
        return jsonify({'message': 'There is no user'})

    user_data = dict()
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['admin'] = user.admin
    user_data['password'] = user.password
    user_data['id'] = user.id

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'])

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password,
                    admin=False, email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': "New user created"})


@token_required
@app.route('/user/<public_id>', methods=['PUT'])
def update_user(current_user, public_id):

    if not current_user.admin and not current_user.public_id == public_id:
        return jsonify({'message': 'You have no permission'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'There is no user'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been updated'})


@token_required
@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(current_user, public_id):

    if not current_user.admin and not current_user.public_id == public_id:
        return jsonify({'message': 'You have no permission'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'There is no user'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted'})


@app.route('/login')
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id},
                           app.config['secret_key'])
        return jsonify({'token': token.decode("UTF-8")})

    return make_response('Could not verify', 401, {"WWW-AUTHENTICATE": "Bearer realm = no token "})


@app.route('/vault/create/<public_id>', methods=['POST'])
@token_required
def vault_create(current_user, public_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'you have no permission'})

    data = request.get_json()

    new_vault = Vault(owner_id=current_user.id, description=data['description'], title=data['title'])

    db.session.add(new_vault)
    db.session.commit()

    return jsonify({'message': 'New vault created'})


@app.route('/vault', methods=['GET'])
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


@app.route('/user_<public_id>/vault_<vault_id>/update/', methods=['PUT'])
@token_required
def vault_update(current_user, public_id, vault_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    data = request.get_json()

    vault = Vault.query.filter_by(vault_id=vault_id).first()

    if not vault:
        return jsonify({'message': 'There is no vault'})

    vault.title = data['title']
    vault.description = data['description']
    vault.owner_id = current_user.id
    db.session.commit()

    return jsonify({'message': 'vault was updated'})


@app.route('/vault/<vault_id>/update/<public_id>', methods=['DELETE'])
@token_required
def delete_vault(current_user, public_id, vault_id):

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    vault = Vault.query.filter_by(vault_id=vault_id).first()

    if not vault:
        return jsonify({'message': 'there is no vault like this'})

    db.session.delete(vault)
    db.session.commit()

    return jsonify({"message": "vault was deleted"})


@app.route('/user_<public_id>/file/create', methods=['POST'])
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


@app.route('/user_<public_id>/vault<vault_id>/file', methods=['POST'])
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


@app.route('/user_<public_id>/file_<file_id>/update')
@token_required
def file_update(current_user, public_id, file_id):

    data = request.get_json()

    if not current_user.public_id == public_id:
        return jsonify({'message': 'permission denied'})

    file = File.query.filter_by(file_id=file_id).first()

    if not file:
        return jsonify({'message': 'there is no such file'})

    file.name = data['name']
    file.description = data['description']

    db.session.commit()

    return jsonify({"message": "file updated"})


if __name__ == '__main__':
    app.run(debug=True)
