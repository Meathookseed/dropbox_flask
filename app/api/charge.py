from flask_classful import FlaskView
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import ResourceMeta
from app.api.service import StripeService
from flask import make_response
from marshmallow import fields

@doc(tags=['Charge'])
class ChargeView(FlaskView, metaclass=ResourceMeta):

    # def get(self):
    #
    #     token = StripeService.token_for_checkout()
    #
    #     return jsonify({'stripeToken':token})

    @doc(tags=['Charge'])
    @use_kwargs({'stripeToken': fields.Str()})
    def post(self, **kwargs):

        StripeService.checkout(**kwargs)

        return make_response("Purchased was succeed", 200)







