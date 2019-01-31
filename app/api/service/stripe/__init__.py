import stripe
from app.api.decorators import token_required
from app.models.models import Stripe
from app.shortcuts import dbsession


class StripeService:

    stripe_keys = {
        'secret_key': "sk_test_MZ8zyYwjAOyfA3qdmyP0OnZw",
    }

    stripe.api_key = stripe_keys['secret_key']

    @staticmethod
    @token_required
    def checkout(current_user, **kwargs):

        email = current_user.email

        customer = stripe.Customer.create(
            email=email,
            source=kwargs['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=500,
            currency='usd',
            description='Flask Charge'
        )

        stripe_entity = Stripe(id=current_user.id, stripe_id=customer.id, token=kwargs['stripeToken'])
        dbsession.add(stripe_entity)
        dbsession.commit()

        return charge
