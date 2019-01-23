from marshmallow import fields

from app.extensions import ma
from app.models.models import File, User, Vault


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File


class VaultSchema(ma.ModelSchema):

    files = fields.Nested(FileSchema, many=True)

    class Meta:
        model = Vault
        fields = ['vault_id','files', 'title', 'vault_self_links', 'description']

    vault_self_links = ma.Hyperlinks({
        'self': ma.URLFor('VaultView:get', id='<vault_id>'),
        'user_vaults': ma.URLFor('VaultView:index', id='<owner_id>')
    })


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        fields = ['username', 'password', 'id', 'public_id', 'vaults', "admin", 'photo']

    vaults = fields.Nested(VaultSchema, many=True)
