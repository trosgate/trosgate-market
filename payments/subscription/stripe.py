# services.py
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class StripeSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Stripe Subscription"


class StripeService:
    @staticmethod
    def create_subscription(user, plan_id, payment_method=None, card_token=None):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if card_token:
            customer = stripe.Customer.create(
                email=user.email,
                source=card_token,
            )
        else:
            customer = stripe.Customer.create(
                email=user.email,
                payment_method=payment_method,
                invoice_settings={
                    'default_payment_method': payment_method,
                },
            )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': plan_id}],
            expand=['latest_invoice.payment_intent'],
        )

        stripe_subscription_id = subscription.id
        stripe_subscription = StripeSubscription.objects.create(user=user, stripe_subscription_id=stripe_subscription_id)

        return stripe_subscription

    @staticmethod
    def charge_user(amount, payment_method, description):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',  # Change to the appropriate currency code
            payment_method=payment_method,
            description=description,
            confirm=True,
        )

        return intent.id

    @staticmethod
    def cancel_subscription(subscription_id):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.delete()

        return True

    @staticmethod
    def refund_payment(payment_intent_id, amount):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        refund = stripe.Refund.create(
            payment_intent=payment_intent_id,
            amount=amount,
        )

        return refund.id

    @staticmethod
    def get_user_subscription(user):
        try:
            return StripeSubscription.objects.get(user=user)
        except StripeSubscription.DoesNotExist:
            return None
