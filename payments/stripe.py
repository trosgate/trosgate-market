from django.contrib.sites.models import Site
from payments.models import MerchantAPIs
import stripe
from account.fund_exception import (
    GatewayModuleNotFound, 
    GatewayNotConfigured, 
    InvalidData
)
from general_settings.currency import get_base_currency_code


class StripeClientConfig:
    currency_notation = 100

    def __init__(self):
        self.name = 'stripe'
        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant
        self.currency = self.default_currency()
        stripe.api_key = self.stripe_secret_key()
        self.stripe = stripe


    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site, stripe_active=True).first()
        return merchant

    def default_currency(self):
        currency = self.site.merchant.merchant.merchant.country.currency.lower()
        return currency if currency else 'usd'

    def stripe_public_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.stripe_public_key
        return None


    def stripe_secret_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.stripe_secret_key
        return None
    

    def stripe_webhook_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.stripe_webhook_key
        return None


    def get_gateway_status(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.stripe_sandbox
        return False
    
    
    def create_payment_intent(self, amount, card_token):
        try:
            payment_intent = self.stripe.PaymentIntent.create(
                amount=int(amount * self.currency_notation),
                currency=self.currency,
                payment_method_types=['card'],
                payment_method_data={
                    'type': 'card',
                    'card': {
                        'token': card_token,
                    },
                },
                capture_method='automatic',  # Set 'manual' if you want to capture later
            )
            return payment_intent.id, payment_intent.client_secret
        except self.stripe.error.StripeError as e:
            raise InvalidData(f"Error! {e}")


    def confirm_payment(self, payment_intent_id):
        try:
            payment_intent = self.stripe.PaymentIntent.confirm(payment_intent_id)
            return payment_intent.status
        except self.stripe.error.StripeError as e:
            raise InvalidData(f"Error! {e}")
    

    def checkout(self, amount, card_token):
        try:
            payment_intent_client_secret = self.create_payment_intent(amount, card_token)
            payment_intent_id = self.stripe.PaymentIntent.retrieve(payment_intent_client_secret).id
            payment_status = self.confirm_payment(payment_intent_id)
            return payment_status
        except self.stripe.error.StripeError as e:
            raise InvalidData(f"Error! {e}")
    

    def subscribe(self, customer_id, plan_id):
        try:
            subscription = self.stripe.Subscription.create(
                customer=customer_id,
                items=[{'plan': plan_id}]
            )
            return subscription.id
        except self.stripe.error.StripeError as e:
            raise InvalidData(f"Error! {e}")


    def cancel_subscription(self, subscription_id):
        try:
            subscription = self.stripe.Subscription.retrieve(subscription_id)
            subscription.delete()
            return True
        except self.stripe.error.StripeError as e:
            raise InvalidData(f"Error! {e}")


    def refund(self, charge_id):
        try:
            refund = self.stripe.Refund.create(
                charge=charge_id
            )
            return refund.id
        except self.stripe.error.StripeError as e:
            raise InvalidData(f"Error! {e}")


    def create_manual_check(self, amount, customer_id):
        try:
            response = self.stripe.Charge.create(
                amount=int(amount * 100),
                currency=self.currency,
                customer=customer_id
            )
            return response.id, response.status
        except (self.stripe.error.StripeError, self.stripe.CardError, self.stripe.InvalidRequestError) as e:
            raise InvalidData(f"Error! {e}")         