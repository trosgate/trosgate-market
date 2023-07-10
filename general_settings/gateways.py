from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import sys
import os
import stripe
import secrets
import requests
from transactions.models import Purchase
from payments.models import MerchantAPIs
from django.conf import settings
from django.contrib.sites.models import Site
import razorpay


def ref_generator():
    new_unique_reference = ''
    generated_reference = secrets.token_urlsafe(30)[:30]
    while not Purchase.objects.filter(unique_reference=generated_reference).exists():
        new_unique_reference = generated_reference
        break
    return new_unique_reference


# PAYPAL PAYMENT GATEWAY
def get_gateway_environment():
    pass


# ------------------> PAYPAL PAYMENT GATEWAY START< ------------------#

class PayPalClientConfig:
    def __init__(self):
        self.name = 'paypal'
        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant

    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site).first()
        return merchant

    def paypal_public_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.paypal_public_key
        return None

    def paypal_secret_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.paypal_secret_key
        return None

    def get_gateway_environment(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.sandbox
        return False

    def paypal_environment(self):
        gateway_environment = self.get_gateway_environment()
        if gateway_environment:
            if gateway_environment:
                environment = SandboxEnvironment(client_id=self.paypal_public_key(), client_secret=self.paypal_secret_key())
            else:
                environment = LiveEnvironment(client_id=self.paypal_public_key(), client_secret=self.paypal_secret_key())
            return environment
        return None

    def paypal_httpclient(self):
        environment = self.paypal_environment()
        if environment:
            return PayPalHttpClient(environment)
        return None

# ------------------> PAYPAL PAYMENT GATEWAY ENDS< ------------------#

# ------------------> STRIPE PAYMENT GATEWAY START< ------------------#
class StripeClientConfig:
    def __init__(self):
        print('Stripe')

    def stripe_public_key(self):
        try:
            return PaymentGateway.objects.get(name='stripe').public_key 
        except:
            return None

    def stripe_secret_key(self):
        try:
            return PaymentGateway.objects.get(name='stripe').secret_key 
        except:
            return None

    def stripe_webhook_key(self):
        try:
            return PaymentGateway.objects.get(name='stripe').webhook_key 
        except:
            return None    

    def stripe_subscription_price_id(self):
        try:
            return PaymentGateway.objects.get(name='stripe').subscription_price_id 
        except:
            return None 


# ------------------> STRIPE PAYMENT GATEWAY ENDS< ------------------#


# ------------------> FLUTTERWAVE PAYMENT GATEWAY START< ------------------#
class FlutterwaveClientConfig:
    def __init__(self):
        print('Flutterwave')

    def flutterwave_public_key(self):
        try:
            return PaymentGateway.objects.get(name='flutterwave').public_key 
        except:
            return None

    def flutterwave_secret_key(self):
        try:
            return PaymentGateway.objects.get(name='flutterwave').secret_key 
        except:
            return None

    def flutterwave_subscription_price_id(self):
        try:
            return PaymentGateway.objects.get(name='flutterwave').subscription_price_id 
        except:
            return None   

    def flutterwave_unique_reference(self):
        return ref_generator()

# ------------------> FLUTTERWAVE PAYMENT GATEWAY ENDS< ------------------#

# ------------------> RAZORPAY PAYMENT GATEWAY START< ------------------#
class RazorpayClientConfig:
    def __init__(self):
        print('Razorpay')

    def razorpay_public_key_id(self):
        try:
            return PaymentGateway.objects.get(name='razorpay').public_key 
        except:
            return None

    def razorpay_secret_key_id(self):
        try:
            return PaymentGateway.objects.get(name='razorpay').secret_key 
        except:
            return None

    def razorpay_subscription_price_id(self):
        try:
            return PaymentGateway.objects.get(name='razorpay').subscription_price_id 
        except:
            return None

    def razorpay_unique_reference(self):
        return ref_generator()

    def get_razorpay_client(self):
        return razorpay.Client(auth=(self.razorpay_public_key_id(), self.razorpay_secret_key_id()))
    
# ------------------> FLUTTERWAVE PAYMENT GATEWAY START< ------------------#