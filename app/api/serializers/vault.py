from app.extensions import ma
from app.models.models import Vault, File
from marshmallow import fields


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File


class VaultSchema(ma.ModelSchema):
    files = fields.Nested(FileSchema, many=True)

    class Meta:
        model = Vault
        fields = ['title', 'description', 'files', '_links', "owner_id"]

    _links = ma.Hyperlinks({
        'self': ma.URLFor('VaultView:get', id_='<vault_id>'),
    })
