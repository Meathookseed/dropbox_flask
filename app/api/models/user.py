from app import db
from werkzeug.security import check_password_hash, generate_password_hash


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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
