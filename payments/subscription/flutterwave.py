# services.py
import requests
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class FlutterwaveSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flutterwave_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Flutterwave Subscription"

class FlutterwaveService:
    @staticmethod
    def create_subscription(user, plan_id, email):
        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            'tx_ref': 'your-transaction-reference',  # Replace with a unique transaction reference
            'order_id': 'your-order-id',  # Replace with a unique order ID
            'amount': 'your-amount',  # Replace with the subscription amount
            'currency': 'NGN',  # Replace with the appropriate currency code
            'payment_type': 'recurring',
            'redirect_url': 'your-redirect-url',  # Replace with the URL to redirect after payment
            'order_ref': 'your-order-reference',  # Replace with a unique order reference
            'billing_name': user.get_full_name(),
            'billing_email': email,
            'billing_phone': 'user-phone-number',  # Replace with the user's phone number
            'billing_address': 'user-address',  # Replace with the user's address
        }

        response = requests.post('https://api.flutterwave.com/v3/charges?type=recurring', json=data, headers=headers)
        result = response.json()

        flutterwave_subscription_id = result.get('data', {}).get('id')
        if flutterwave_subscription_id:
            subscription = FlutterwaveSubscription.objects.create(user=user, flutterwave_subscription_id=flutterwave_subscription_id)
            return subscription
        else:
            return None

    @staticmethod
    def cancel_subscription(subscription_id):
        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.post(f'https://api.flutterwave.com/v3/subscriptions/{subscription_id}/cancel', headers=headers)
        result = response.json()

        return result.get('status') == 'success'

    @staticmethod
    def refund_payment(transaction_id, amount):
        # Flutterwave's API for refunds might be different. Refer to the documentation.
        # You might need to provide the payment ID and refund amount.
        pass

    @staticmethod
    def charge_user(amount, email):
        # Similar to creating a subscription, you can create a one-time payment here.
        # Refer to Flutterwave's documentation for the correct API endpoint and payload.
        pass

    @staticmethod
    def verify_payment(reference):
        # Flutterwave may provide a mechanism to verify payments. Check the documentation.
        pass

    @staticmethod
    def get_user_subscription(user):
        try:
            return FlutterwaveSubscription.objects.get(user=user)
        except FlutterwaveSubscription.DoesNotExist:
            return None
