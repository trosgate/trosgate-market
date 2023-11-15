from django.contrib.sites.models import Site
from payments.models import MerchantAPIs
import stripe
from account.fund_exception import (
    GatewayModuleNotFound, 
    GatewayNotConfigured, 
    InvalidData
)
from general_settings.currency import get_base_currency_code
import uuid
import requests



class FlutterwaveClientConfig:
    currency_notation = 100
    FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"

    def __init__(self):
        self.name = 'flutterwave'
        self.currency = get_base_currency_code() if get_base_currency_code() else 'NGN'
        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant
        self.flutterwave_public_key = self.flutterwave_public_key()
        self.flutterwave_secret_key = self.flutterwave_secret_key()
        self.reference = "ref-" + str(uuid.uuid4())[:18] 

        self.headers = {
            "Authorization": f"Bearer {self.flutterwave_secret_key}",
            "Content-Type": "application/json",
        }


    def _make_api_request(self, method, endpoint, data=None):
        url = f"{self.FLUTTERWAVE_BASE_URL}/{endpoint}"
        try:
            response = method(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Handle the error here or re-raise the exception if needed
            print("Error:", e)
            return None

    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site, stripe_active=True).first()
        return merchant


    def flutterwave_public_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.flutterwave_public_key
        return None


    def flutterwave_secret_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.flutterwave_secret_key
        return None
    

    def create_payment(self, amount, redirect_url):
        print('Reference ::', self.reference)
        endpoint = F"/payments"
        payload = {
            "tx_ref": self.reference,
            "amount": amount,
            "currency": self.currency,
            "redirect_url": redirect_url,
        }
        response = self._make_api_request(requests.post, endpoint, data=payload)
        return response, self.reference 

    def verify_payment(self, transaction_id):
        endpoint = f"transactions/{transaction_id}/verify"
        return self._make_api_request(requests.get, endpoint)


    def create_subscription(self, amount, interval, currency, customer_email, plan_id):
        endpoint = "subscriptions"
        payload = {
            "amount": amount,
            "interval": interval,
            "currency": currency,
            "customer_email": customer_email,
            "plan": plan_id,
            # Add more payload parameters as needed
        }
        return self._make_api_request(requests.post, endpoint, data=payload)

    def refund_payment(self, transaction_id, amount=None):
        endpoint = f"transactions/{transaction_id}/refund"
        payload = {}
        if amount:
            payload["amount"] = amount
        return self._make_api_request(requests.post, endpoint, data=payload)