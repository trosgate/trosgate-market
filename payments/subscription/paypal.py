# services.py
import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models


class PayPalSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paypal_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s PayPal Subscription"


class PayPalService:
    @staticmethod
    def create_subscription(user, plan_id):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET,
        })

        plan = paypalrestsdk.Plan.find(plan_id)
        agreement = paypalrestsdk.Agreement({
            "name": plan.name,
            "description": plan.description,
            "start_date": "2023-01-01T00:00:00Z",  # Set a future date
            "payer": {"payment_method": "paypal"},
            "plan": {"id": plan.id},
            "shipping_address": {"line1": "1234 Main St", "city": "Gotham", "state": "NY", "postal_code": "10001", "country_code": "US"},
        })

        if agreement.create():
            subscription = PayPalSubscription.objects.create(user=user, paypal_subscription_id=agreement.id)
            return subscription
        else:
            return None

    @staticmethod
    def execute_agreement(token):
        agreement = paypalrestsdk.Agreement.execute(token)
        return agreement.id if agreement.state == "Active" else None

    @staticmethod
    def cancel_subscription(subscription_id):
        agreement = paypalrestsdk.Agreement.find(subscription_id)
        if agreement.cancel():
            return True
        else:
            return False

    @staticmethod
    def refund_payment(transaction_id, amount):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET,
        })

        sale = paypalrestsdk.Sale.find(transaction_id)

        refund = sale.refund({
            "amount": {
                "total": amount,
                "currency": "USD",  # Change to the appropriate currency code
            },
        })

        return refund.id if refund.state == "completed" else None

    @staticmethod
    def get_user_subscription(user):
        try:
            return PayPalSubscription.objects.get(user=user)
        except PayPalSubscription.DoesNotExist:
            return None
