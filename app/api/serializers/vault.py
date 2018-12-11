from app.extensions import ma
from app.models.models import Vault


class VaultSchema(ma.ModelSchema):
    class Meta:
        model = Vault
