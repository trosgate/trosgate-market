import requests
import json
import base64
import time
import hashlib
import hmac
import uuid


class MTNCheckout:
    def __init__(self):
        self.name = "mtn"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
            ("mtn", "MTN Mobile Money"),
        )

        # Load the MTN Mobile Money API keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="mtn")
            self.api_user_id = payment_gateway.api_user_id
            self.api_key = payment_gateway.api_key
            self.subscription_key = payment_gateway.subscription_key
            self.callback_url = payment_gateway.callback_url
        except PaymentGateway.DoesNotExist:
            pass

    def create_checkout(self, amount, currency="UGX", customer_phone=None):
        timestamp = str(int(time.time() * 1000))
        transaction_reference = str(uuid.uuid4())
        reference_id = str(uuid.uuid4())
        api_key_bytes = self.api_key.encode('utf-8')
        secret_bytes = self.api_secret.encode('utf-8')
        raw_signature = '{}{}{}{}{}'.format(self.api_user_id, self.subscription_key, timestamp, transaction_reference, amount)
        signature = base64.b64encode(hmac.new(secret_bytes, raw_signature.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'X-Reference-Id': reference_id,
            'X-Target-Environment': 'sandbox',
            'X-Timestamp': timestamp,
            'X-Callback-Url': self.callback_url,
            'Content-Type': 'application/json',
        }

        data = {
            "amount": amount,
            "currency": currency,
            "externalId": transaction_reference,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": customer_phone,
            }
        }

        response = requests.post('https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay',
                                 headers=headers,
                                 data=json.dumps(data),
                                 verify=False)

        if response.status_code == 202:
            return {
                "reference_id": reference_id,
                "transaction_reference": transaction_reference,
                "amount": amount,
                "currency": currency,
                "name": "MTN Mobile Money",
                "description": "Pay with MTN Mobile Money",
                "phone": customer_phone,
                "callback_url": self.callback_url,
                "signature": signature,
            }
        else:
            # Handle any MTN Mobile Money checkout creation errors here
            return f"Error creating MTN Mobile Money checkout: {response.text}"
