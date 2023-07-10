import requests

import requests


# VERIFY FIRST BEFORE SAVING APPROACH USING API
class PayPalClient:
    SANDBOX_API_BASE_URL = 'https://api.sandbox.paypal.com'
    LIVE_API_BASE_URL = 'https://api.paypal.com'

    def __init__(self, client_id, client_secret, use_sandbox=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_sandbox = use_sandbox
        self.api_base_url = self.SANDBOX_API_BASE_URL if use_sandbox else self.LIVE_API_BASE_URL

    def get_access_token(self):
        # Obtain the access token using your client credentials
        # ...
        pass

    def get_payment_status(self, payment_id):
        url = f"{self.api_base_url}/v2/payments/payment/{payment_id}"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.get_access_token()}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            payment_status = response.json()["status"]
            return payment_status
        else:
            raise Exception("Failed to retrieve PayPal payment details")

# VIEW CODE
def paypalStatusCheck():
    paypal_client = PayPalClient(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET', use_sandbox=True)

    # Get the payment status using the payment ID
    payment_id = 'PAYMENT_ID_FROM_PAYPAL'
    payment_status = paypal_client.get_payment_status(payment_id)

    # Verify the payment status
    if payment_status == 'approved':
        pass
        # Payment is successful, save it in your database
    else:
        # Payment is not approved or failed, handle accordingly
        pass

















class PayPalClient:
    SANDBOX_API_BASE_URL = 'https://api.sandbox.paypal.com'
    LIVE_API_BASE_URL = 'https://api.paypal.com'

    def __init__(self, client_id, client_secret, use_sandbox=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_sandbox = use_sandbox
        self.api_base_url = self.SANDBOX_API_BASE_URL if use_sandbox else self.LIVE_API_BASE_URL

    def get_access_token(self):
        url = f"{self.api_base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, data=data, auth=(self.client_id, self.client_secret), headers=headers)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Failed to retrieve PayPal access token")

    def create_order(self, amount, currency):
        url = f"{self.api_base_url}/v2/checkout/orders"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.get_access_token()}"}
        data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount)
                    }
                }
            ]
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return response.json()["id"]
        else:
            raise Exception("Failed to create PayPal order")

    def capture_order(self, order_id):
        url = f"{self.api_base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.get_access_token()}"}

        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to capture PayPal order")

    def create_subscription(self, plan_id, subscriber_email, currency="USD"):
        url = f"{self.api_base_url}/v1/billing/subscriptions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.get_access_token()}"}
        data = {
            "plan_id": plan_id,
            "subscriber": {
                "email_address": subscriber_email
            },
            "application_context": {
                "brand_name": "Your Brand Name",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "SUBSCRIBE_NOW",
                "payment_method": {
                    "payer_selected": "PAYPAL",
                    "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                },
                "return_url": "https://yourdomain.com/success",
                "cancel_url": "https://yourdomain.com/cancel"
            }
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return response.json()["id"]
        else:
            raise Exception("Failed to create PayPal subscription")
