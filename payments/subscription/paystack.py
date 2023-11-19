# services.py
import requests
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class PaystackSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paystack_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Paystack Subscription"

class PaystackService:
    @staticmethod
    def make_paystack_request(method, endpoint, data=None):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        url = f'https://api.paystack.co/{endpoint}'
        response = requests.request(method, url, json=data, headers=headers)
        result = response.json()

        return result

    @staticmethod
    def create_subscription(user, plan_id, email):
        data = {
            'email': email,
            'plan': plan_id,
        }

        result = PaystackService.make_paystack_request('post', 'subscription', data)

        paystack_subscription_id = result.get('data', {}).get('id')
        if paystack_subscription_id:
            subscription = PaystackSubscription.objects.create(user=user, paystack_subscription_id=paystack_subscription_id)
            return subscription
        else:
            return None

    @staticmethod
    def cancel_subscription(subscription_id):
        result = PaystackService.make_paystack_request('post', f'subscription/disable/{subscription_id}')
        return result.get('status') == True

    @staticmethod
    def refund_payment(transaction_id, amount):
        data = {
            'transaction': transaction_id,
            'amount': amount * 100,  # Paystack requires the amount in kobo
        }

        result = PaystackService.make_paystack_request('post', 'refund', data)
        return result.get('data', {}).get('id')

    @staticmethod
    def charge_user(amount, email, reference):
        data = {
            'email': email,
            'amount': amount * 100,  # Paystack requires the amount in kobo
            'reference': reference,
        }

        result = PaystackService.make_paystack_request('post', 'transaction/initialize', data)
        authorization_url = result.get('data', {}).get('authorization_url')
        return authorization_url

    @staticmethod
    def verify_transaction(reference):
        result = PaystackService.make_paystack_request('get', f'transaction/verify/{reference}')
        return result.get('data', {}).get('status') == 'success'

    @staticmethod
    def get_user_subscription(user):
        try:
            return PaystackSubscription.objects.get(user=user)
        except PaystackSubscription.DoesNotExist:
            return None
