from flask_classy import FlaskView

from app.api.service.vault import VaultService
from app.api.serializers.vault import VaultSchema

from flask import request

from flask_apispec.annotations import marshal_with, doc


class VaultView(FlaskView):



    @marshal_with(VaultSchema(many=True))
    @doc(description='Get List of all users vaults')
    def index(self, id_):
        """List of users"""
        return VaultService.list(id_=id_)

    @marshal_with(VaultSchema())
    def get(self, id_):
        """Retrieve one user"""
        return VaultService.one(id_=id_)


    @doc(description='Creates new user')
    def post(self, id_):
        """Create User"""
        data = request.get_json()
        return VaultService.create(data=data, id_=id_)

    @doc(description='Updates user')
    @marshal_with(VaultSchema())
    def patch(self, public_id):
        """Update user"""
        data = request.get_json()
        return VaultService.update(data, public_id)

    @doc(description='Deletes user')
    def delete(self, public_id):
        """Delete User"""
        return VaultService.delete(public_id)
