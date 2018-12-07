from app import db

class Vault(db.Model):
    vault_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String())
    files = db.relationship('File')