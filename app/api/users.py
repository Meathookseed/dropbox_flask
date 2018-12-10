from flask_classy import FlaskView, route
from flask_apispec.annotations import marshal_with
from flask import request

from app.api.service.user import UserService
from app.api.serializers.user import UserSchema
from app.api.decorators.token import token_required


class UserView(FlaskView):

    @route('users/')
    @marshal_with(UserSchema(many=True))
    @token_required
    def index(self, current_user):
        return UserService.list(current_user)

    @route('user/<public_id>')
    @marshal_with(UserSchema())
    @token_required
    def get(self, current_user, public_id):
        return UserService.one(current_user, public_id)

    @route('create_user/')
    def post(self):
        data = request.get_json()
        return UserService.create(data)

