from app.extensions import ma
from app.models.models import File


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File
        fields = ['vault_id', "data", "name", "description", "file_id"]
