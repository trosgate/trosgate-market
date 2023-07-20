from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import requests
from payments.models import MerchantAPIs
from django.conf import settings
from django.contrib.sites.models import Site


class PayPalClientConfig:
    def __init__(self):
        self.name = 'paypal'
        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant

    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site, paypal_active=True).first()
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


    def get_base_url(self):
        sandbox_url = 'https://api.sandbox.paypal.com' 
        live_url = 'https://api.paypal.com'
        gateway = self.get_payment_gateway()
        if gateway.sandbox:
            return sandbox_url
        return live_url
  

    def get_access_token(self):
        # print('paypal_secret_key :', self.paypal_secret_key())
        # print('paypal_public_key :', self.paypal_public_key())
        url = f'{self.get_base_url()}/v1/oauth2/token'
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }
        data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, auth=(self.paypal_public_key(), self.paypal_secret_key()), data=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f'Error: {response.text}')


    def create_order(self, amount, currency='USD', description='purchase of service'):
        url = f'{self.get_base_url()}/v2/checkout/orders'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        data = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': {
                        'currency_code': currency,
                        'value': amount,
                    },
                    'description': description,
                }
            ]
        }
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            return response.json()['id']
        else:
            raise Exception(f'Failed to create order with PayPal: {response.text}')


    def capture_order(self, order_id):
        
        url = f'{self.get_base_url()}/v2/checkout/orders/{order_id}/capture'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            
            return response.json()
        else:
            raise Exception(f'Failed to capture payment with PayPal: {response.text}')


    def create_subscription(self, plan_id, quantity=1):
        url = f'{self.get_base_url()}/v1/billing/subscriptions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        data = {
            'plan_id': plan_id,
            'quantity': quantity,
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return response.json()['id']
        else:
            raise Exception(f'Failed to create subscription with PayPal: {response.text}')


    def cancel_subscription(self, subscription_id):
        url = f'{self.get_base_url()}/v1/billing/subscriptions/{subscription_id}/cancel'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 204:
            return True
        else:
            raise Exception(f'Failed to cancel subscription with PayPal: {response.text}')

    def refund_payment(self, sale_id, amount, currency='USD', note=''):
        url = f'{self.get_base_url()}/v2/payments/captures/{sale_id}/refund'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        data = {
            'amount': {
                'currency_code': currency,
                'value': amount,
            },
            'note_to_payer': note,
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f'Failed to process refund with PayPal: {response.text}')
