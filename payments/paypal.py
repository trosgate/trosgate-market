from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import requests
import paypalrestsdk
from payments.models import MerchantAPIs
from django.conf import settings
from django.contrib.sites.models import Site
import requests
from requests.auth import HTTPBasicAuth
import json



class PayPalClientConfig:
    
    TEST_CARD = 4000000000003220
    TEST_CVC = 234
    TEST_DATE = 'PUT FUTURE DATE HERE DYNAMICALLY'

    def __init__(self):
        self.name = 'paypal'
        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant
        self.currency = self.default_currency()


    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site, paypal_active=True).first()
        return merchant

    def default_currency(self):
        currency = self.site.merchant.merchant.merchant.country.currency.lower()
        return currency if currency else 'usd'

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


    def create_order(self, amount, description='purchase of service'):
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
                        'currency_code': self.currency,
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


    def create_paypal_plan(subscription): #This assumes Restsdk and that i have a model object
        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET,
        })

        plan = paypalrestsdk.Plan({
            "name": subscription.name,
            "description": subscription.description,
            "type": "fixed",
            "payment_definitions": [
                {
                    "name": "Regular payment definition",
                    "type": "REGULAR",
                    "frequency": "MONTH",
                    "frequency_interval": "1",
                    "amount": {
                        "currency": "USD",
                        "value": str(subscription.price),
                    },
                    "cycles": "0",
                }
            ],
            "merchant_preferences": {
                "return_url": "http://your-return-url.com",
                "cancel_url": "http://your-cancel-url.com",
                "auto_bill_amount": "YES",
                "initial_fail_amount_action": "CONTINUE",
                "max_fail_attempts": "2",
            },
        })

        if plan.create():
            subscription.paypal_plan_id = plan.id
            subscription.save()
            return plan
        else:
            return None


    def get_approval_url(plan):
        for link in plan.links:
            if link.rel == "approval_url":
                return link.href

        return None


    def create_paypal_plan(plan_name, description, price):
        url = 'https://api.sandbox.paypal.com/v1/billing/plans'  
        # Use 'https://api.paypal.com/v1/billing/plans' for live mode
        headers = {
            'Content-Type': 'application/json',
        }
        # REMEMBER TO CHANGE HTTPBasicAuth TO AUTHORIZATION IMPLEMENTED ABOVE
        auth = HTTPBasicAuth('YOUR_PAYPAL_CLIENT_ID', 'YOUR_PAYPAL_CLIENT_SECRET')

        data = {
            # "product_id": "PROD-PRODUCT_ID",  # Replace with your product ID
            "name": plan_name,
            "description": description,
            "billing_cycles": [
                {
                    "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 0,
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": price,
                            "currency_code": "USD"
                        }
                    }
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee": {
                    "value": "0",
                    "currency_code": "USD"
                },
                "setup_fee_failure_action": "CONTINUE",
                "payment_failure_threshold": 3
            },
            "taxes": {
                "percentage": "0",
                "inclusive": False
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), auth=auth)
        if response.status_code == 201:
            plan_id = response.json()['id']
            return plan_id
        else:
            raise Exception(f'Failed to create PayPal plan: {response.text}')


    # Example usage:
    # plan_name = "Monthly Plan"
    # description = "Monthly subscription plan"
    # price = "9.99"

    # plan_id = create_paypal_plan(plan_name, description, price)
    # print(f"Created PayPal plan with ID: {plan_id}")


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
