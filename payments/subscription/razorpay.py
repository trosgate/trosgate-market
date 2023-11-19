# services.py
import razorpay
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class RazorpaySubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    razorpay_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Razorpay Subscription"

class RazorpayService:
    @staticmethod
    def create_subscription(user, plan_id, email):
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        data = {
            'plan_id': plan_id,
            'customer_email': email,
        }

        subscription = client.subscription.create(data=data)

        razorpay_subscription_id = subscription.get('id')
        if razorpay_subscription_id:
            subscription = RazorpaySubscription.objects.create(user=user, razorpay_subscription_id=razorpay_subscription_id)
            return subscription
        else:
            return None

    @staticmethod
    def cancel_subscription(subscription_id):
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        subscription = client.subscription.fetch(subscription_id)
        subscription.cancel()

        return True

    @staticmethod
    def refund_payment(payment_id, amount):
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        refund = client.payment.refund(payment_id, {'amount': amount * 100})  # Razorpay requires the amount in paisa

        return refund.get('id')

    @staticmethod
    def charge_user(amount, email, description):
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        data = {
            'amount': amount * 100,  # Razorpay requires the amount in paisa
            'currency': 'INR',
            'receipt': description,
            'payment_capture': 1,
            'notes': {'email': email},
        }

        payment = client.order.create(data=data)

        return payment.get('id')

    @staticmethod
    def verify_payment(payment_id, signature, payload):
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_signature': signature,
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': payload.get('razorpay_order_id'),
            })
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_user_subscription(user):
        try:
            return RazorpaySubscription.objects.get(user=user)
        except RazorpaySubscription.DoesNotExist:
            return None
