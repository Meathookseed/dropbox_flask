from app.models.models import User
from app.extensions import ma


class PhotoSerializer(ma.ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'photo']
