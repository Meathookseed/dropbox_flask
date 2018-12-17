from app.extensions import ma
from app.models.models import File


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File
        fields = ['vault_id', "owner_url", "data", "name", "description"]

    owner_url = ma.Hyperlinks({
        'owner_url': ma.URLFor('UserView:get', id='<owner_id>')
    })
