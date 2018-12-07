from app import db


class File(db.Model):
    file_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vault_id = db.Column(db.Integer, db.ForeignKey('vault.vault_id'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String())
    data = db.Column(db.LargeBinary)
