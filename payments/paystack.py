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
from general_settings.models import ExachangeRateAPI


class PaystackClientConfig:
    currency_notation = 100
    PAYSTACK_BASE_URL = "https://api.paystack.co"


    def __init__(self):
        self.name = 'paystack'
        self.currency = get_base_currency_code() if get_base_currency_code() else 'NGN'

        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant
        self.paystack_public_key = self.paystack_public_key()
        self.paystack_secret_key = self.paystack_secret_key()
        self.reference = "ref-" + str(uuid.uuid4())[:18] 

        self.headers = {
            "Authorization": f"Bearer {self.paystack_secret_key}",
            "Content-Type": "application/json",
        }


    def _make_api_request(self, method, endpoint, data=None):
        url = f"{self.PAYSTACK_BASE_URL}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.paystack_secret_key}',
            'Content-Type': 'application/json',
        }

        try:
            response = method(url, headers=headers, json=data)
            print(response)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Handle the error here or re-raise the exception if needed
            print("Error:", e)
            return None


    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site, paystack_active=True).first()
        return merchant


    def paystack_public_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.paystack_public_key
        return None
    

    def paystack_secret_key(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.paystack_secret_key
        return None


    def create_order(self, amount, currency):
        if not self.paystack_secret_key:
            raise InvalidData("Paystack secret key not found")

        data = {
            'amount': amount,
            'currency': currency,
        }

        try:
            response_data = self._make_api_request(requests.post, 'transaction/initialize', data)
            if response_data and response_data['status']:
                transaction_reference = response_data['data']['reference']
                return transaction_reference
            else:
                raise InvalidData(f"Failed to create Paystack order: {response_data['message']}")
        except Exception as e:
            raise InvalidData(f"Error creating Paystack order: {e}")


    def capture_payment(self, payment_reference, amount):
        if not self.paystack_secret_key:
            raise InvalidData("Paystack secret key not found")

        data = {
            'amount': amount * 100,  # Convert amount to kobo
        }

        try:
            response_data = self._make_api_request(requests.post, f'transaction/verify/{payment_reference}', data)
            if response_data and response_data['status'] and response_data['data']['status'] == 'success':
                return True
            else:
                raise InvalidData(f"Payment verification failed: {response_data['message']}")
        except Exception as e:
            raise InvalidData(f"Error verifying payment: {e}")


    def get_supported_currencies(self):
        api_url = f"{self.PAYSTACK_BASE_URL}/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {self.paystack_secret_key}',
            'Content-Type': 'application/json',
        }
        response = requests.get(api_url, headers=headers)
        print(response)
        # if response and response['status']:
        #     supported_currencies = response_data['data']['currencies']
        return response

        # return None
    # def get_supported_currencies(self):
    #     api_url = f"transaction/initialize"

    #     response_data = self._make_api_request(requests.get, api_url)
    #     if response_data and response_data['status']:
    #         supported_currencies = response_data['data']['currencies']
    #         return supported_currencies

    #     return None
    
    # def get_supported_currencies(self):
    #     base_url = 'https://api.paystack.co/'

    #     # Construct the API URL
    #     api_url = f"{base_url}transaction/initialize"

    #     headers = {
    #         'Authorization': f'Bearer {self.paystack_secret_key}',
    #     }

    #     try:
    #         response = requests.get(api_url, headers=headers)
    #         print(response)
    #         # Check if the API call was successful
    #         if response.status_code == 200:
    #             data = response.json()
    #             supported_currencies = data['data']['currencies']
    #             return supported_currencies

    #     except requests.RequestException as e:
    #         # Handle request exception or re-raise it if needed
    #         print("Error:", e)

    #     return None



    # def get_exchange_rates_key():
    #     currency_key = ExachangeRateAPI.objects.filter(status=True).first()
    #     if currency_key:
    #         return currency_key.exchange_rates_api_key
    #     return ''

    
    # def get_exchange_rates_path(self, from_currency_code):
    #     url_path = 'https://v6.exchangerate-api.com/v6/%s/latest/%s'
    #     url = url_path % (self.get_exchange_rates_key(), from_currency_code)
    #     r = requests.get(url)
    #     print('status:', r.status_code)
    #     if r.status_code == 200:
    #         return r.json()
    #     return ''

    # def get_conversion_rate(self, from_currency_code, to_currency):
    #     return self.get_exchange_rates_path(from_currency_code)['conversion_rates'][to_currency]
      
    # def get_converted_amount(self, from_currency_code, to_currency, target_amount):
    #     converted_amount = round((target_amount) * (self.get_conversion_rate(from_currency_code.upper(), to_currency.upper())), 2)
    #     return converted_amount