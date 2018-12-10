from app import ma
from app.models.models import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

