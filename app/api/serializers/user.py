from app.extensions import ma
from app.models.models import User, Vault
from marshmallow import fields


class VaultSchema(ma.ModelSchema):
    class Meta:
        model = Vault


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        fields = ['username', 'password', 'id', 'public_id', 'vaults', 'links']

    vaults = fields.Nested(VaultSchema, many=True)

    links = ma.Hyperlinks({
        'self_url': ma.URLFor('UserView:get', public_id='<public_id>')
            })


