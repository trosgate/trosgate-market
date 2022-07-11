from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import sys
import os
import stripe
import secrets
import requests
from transactions.models import Purchase
from general_settings.models import PaymentAPIs
from django.conf import settings

import razorpay

def ref_generator():
    new_unique_reference = ''
    generated_reference = secrets.token_urlsafe(30)[:30]
    while not Purchase.objects.filter(unique_reference=generated_reference).exists():
        new_unique_reference = generated_reference
        break
    return new_unique_reference

# def ref_generator():
#     generated_reference = secrets.token_urlsafe(30)[:30]
#     similar_ref = Purchase.objects.filter(unique_reference=generated_reference)
#     if not similar_ref:
#         new_unique_reference = generated_reference
#     return new_unique_reference
  
# PAYPAL PAYMENT GATEWAY
def get_gateway_environment():
    try:
        return PaymentAPIs.objects.get(id=1).sandbox
    except:
        return True


class PayPalClientConfig:
    def __init__(self):
        print('PayPal')

    def paypal_public_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).paypal_public_key 
        except:
            return None

    def paypal_secret_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).paypal_secret_key 
        except:
            return None

    def paypal_subscription_price_id(self):
        try:
            return PaymentAPIs.objects.get(id=1).paypal_subscription_price_id 
        except:
            return None

    def paypal_environment(self):
        environment = ''
        if get_gateway_environment() == True:
            environment = SandboxEnvironment(client_id=self.paypal_public_key(), client_secret=self.paypal_secret_key())
        else:
            environment = LiveEnvironment(client_id=self.paypal_public_key(), client_secret=self.paypal_secret_key())
        return environment                        

    def paypal_httpclient(self):
        return PayPalHttpClient(self.paypal_environment())

    def paypal_unique_reference(self):
        return ref_generator()
       



# STRIPE PAYMENT GATEWAY
#Stripe will handle test and live scenarios
class StripeClientConfig:
    def __init__(self):
        print('Stripe')

    def stripe_public_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).stripe_public_key 
        except:
            return None

    def stripe_secret_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).stripe_secret_key 
        except:
            return None

    def stripe_webhook_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).stripe_webhook_key 
        except:
            return None    

    def stripe_subscription_price_id(self):
        try:
            return PaymentAPIs.objects.get(id=1).stripe_subscription_price_id 
        except:
            return None 


    def stripe_unique_reference(self):
        return ref_generator()


# FLUTTERWAVE PAYMENT GATEWAY
class FlutterwaveClientConfig:
    def __init__(self):
        print('Flutterwave')

    def flutterwave_public_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).flutterwave_public_key 
        except:
            return None

    def flutterwave_secret_key(self):
        try:
            return PaymentAPIs.objects.get(id=1).flutterwave_secret_key 
        except:
            return None

    def flutterwave_subscription_price_id(self):
        try:
            return PaymentAPIs.objects.get(id=1).flutterwave_subscription_price_id 
        except:
            return None    

    def flutterwave_secret_hash(self):
        try:
            return PaymentAPIs.objects.get(id=1).flutterwave_secret_hash 
        except:
            return None    

    def flutterwave_unique_reference(self):
        return ref_generator()


# STRIPE PAYMENT GATEWAY
class RazorpayClientConfig:
    def __init__(self):
        print('Razorpay')

    def razorpay_public_key_id(self):
        try:
            return PaymentAPIs.objects.get(id=1).razorpay_public_key_id 
        except:
            return None

    def razorpay_secret_key_id(self):
        try:
            return PaymentAPIs.objects.get(id=1).razorpay_secret_key_id 
        except:
            return None

    def razorpay_subscription_price_id(self):
        try:
            return PaymentAPIs.objects.get(id=1).razorpay_subscription_price_id 
        except:
            return None

    def razorpay_unique_reference(self):
        return ref_generator()

    def get_razorpay_client(self):
        return razorpay.Client(auth=(self.razorpay_public_key_id(), self.razorpay_secret_key_id()))