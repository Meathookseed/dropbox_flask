from marshmallow import fields

from app.extensions import ma


class LoginSchema(ma.Schema):
    id = fields.Int()
    token = fields.Str()
