from marshmallow import fields

from app.extensions import ma
from app.models.models import File, Vault


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File


class VaultSchema(ma.ModelSchema):

    files = fields.Nested(FileSchema, many=True)

    class Meta:
        model = Vault
        fields = ['title', 'description', 'files',"vault_id"]
