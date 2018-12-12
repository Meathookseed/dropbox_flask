from app.extensions import ma
from app.models.models import User, Vault, File
from marshmallow import fields

class FileSchema(ma.ModelSchema):
    class Meta:
        model = File


class VaultSchema(ma.ModelSchema):

    files = fields.Nested(FileSchema, many=True)

    class Meta:
        model = Vault
        fields = ['files', 'title', 'vault_self_links']

    vault_self_links = ma.Hyperlinks({
        'self': ma.URLFor('VaultView:get', id_='<vault_id>'),
        'user_vaults': ma.URLFor('VaultView:index', id_='<owner_id>')
    })


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        fields = ['username', 'password', 'id', 'public_id', 'vaults', '_links', "admin"]

    vaults = fields.Nested(VaultSchema, many=True)

    _links = ma.Hyperlinks({
        'user_self_url': ma.URLFor('UserView:get', id_='<id>')
            })


