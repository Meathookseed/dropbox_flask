from app.extensions import ma
from app.models.models import User


class PhotoSerializer(ma.ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'photo']
