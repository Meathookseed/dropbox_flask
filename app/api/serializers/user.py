
from marshmallow import Schema,fields, ValidationError


class VaultSchema(Schema):
    vault_id = fields.Integer(dump_only=True)
    owner_id = fields.Integer(dump_only=True)
    title = fields.Str()
    description = fields.Str()

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    public_id = fields.String()
    username = fields.String()
    password = fields.Str()
    email = fields.Email()
    files = fields.Int()
    photo = fields.Str()
    admin = fields.Bool()
    vaults = fields.Nested(VaultSchema)


