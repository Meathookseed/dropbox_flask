from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    vaults = db.relationship('Vault')
    files = db.relationship('File')
    photo = db.Column(db.LargeBinary)
    admin = db.Column(db.Boolean)


class Vault(db.Model):
    vault_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
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
