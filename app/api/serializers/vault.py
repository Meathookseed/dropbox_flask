from app.extensions import ma
from app.models.models import Vault, File


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File


class VaultSchema(ma.ModelSchema):
    files = FileSchema(many=True)

    class Meta:
        model = Vault
        fields = ['title', 'description', 'files', '_links']

    _links = ma.Hyperlinks({
        'self':ma.URLFor('VaultView:get', id_='<vault_id>'),
    })
