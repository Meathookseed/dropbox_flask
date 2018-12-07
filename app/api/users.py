from flask_classy import FlaskView
from flask_apispec.annotations import marshal_with
from app.api.service.user import UserService
from app.api.serializers.user import UserSchema


class UserView(FlaskView):

    @marshal_with(UserSchema)
    def index(self):
        return UserService.list()




