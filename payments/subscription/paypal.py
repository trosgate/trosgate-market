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
    def create_subscription(user, plan_id, email):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            'email': email,
            'plan': plan_id,
        }

        response = requests.post('https://api.paystack.co/subscription', json=data, headers=headers)
        result = response.json()

        paystack_subscription_id = result.get('data', {}).get('id')
        if paystack_subscription_id:
            subscription = PaystackSubscription.objects.create(user=user, paystack_subscription_id=paystack_subscription_id)
            return subscription
        else:
            return None

    @staticmethod
    def cancel_subscription(subscription_id):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.post(f'https://api.paystack.co/subscription/disable/{subscription_id}', headers=headers)
        result = response.json()

        return result.get('status') == True

    @staticmethod
    def refund_payment(transaction_id, amount):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            'transaction': transaction_id,
            'amount': amount * 100,  # Paystack requires the amount in kobo
        }

        response = requests.post('https://api.paystack.co/refund', json=data, headers=headers)
        result = response.json()

        return result.get('data', {}).get('id')

    @staticmethod
    def charge_user(amount, email, reference):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            'email': email,
            'amount': amount * 100,  # Paystack requires the amount in kobo
            'reference': reference,
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
        result = response.json()

        authorization_url = result.get('data', {}).get('authorization_url')
        return authorization_url

    @staticmethod
    def verify_transaction(reference):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        result = response.json()

        return result.get('data', {}).get('status') == 'success'

    @staticmethod
    def get_user_subscription(user):
        try:
            return PaystackSubscription.objects.get(user=user)
        except PaystackSubscription.DoesNotExist:
            return None
