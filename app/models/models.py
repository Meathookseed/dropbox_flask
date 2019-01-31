from app.extensions import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String())
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    vaults = db.relationship('Vault', cascade='all,delete')
    files = db.relationship('File', cascade='all,delete')
    stripe = db.relationship('Stripe', cascade='all,delete')
    photo = db.Column(db.String(100))
    admin = db.Column(db.Boolean)


class Vault(db.Model):
    vault_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String())
    files = db.relationship('File', cascade='all,delete')


class File(db.Model):
    file_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vault_id = db.Column(db.Integer, db.ForeignKey('vault.vault_id'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String())
    data = db.Column(db.String(), unique=True)


class Stripe(db.Model):

    def __init__(self, id, stripe_id, token):
        self.id = id
        self.stripe_id = stripe_id
        self.token = token

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    stripe_id = db.Column(db.String(150), unique=True, nullable=False,autoincrement=False)
    token = db.Column(db.String(150), unique=True, nullable=False)
