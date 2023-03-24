from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
import uuid

from payments.models import PaymentGateway

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

class PayPalCheckout:
    def __init__(self):
        self.name = "paypal"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
        )
        # Load the PayPal keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="paypal")
            self.paypal_client_id = payment_gateway.client_id
            self.paypal_client_secret = payment_gateway.client_secret
            paypalrestsdk.configure({
                "mode": "sandbox",
                "client_id": self.paypal_client_id,
                "client_secret": self.paypal_client_secret
            })
        except PaymentGateway.DoesNotExist:
            raise Exception("PayPal payment gateway not found in the database")

    def create_checkout(self, amount, currency="USD", description="", return_url=None, cancel_url=None):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "transactions": [{
                "amount": {
                    "total": "{:.2f}".format(amount),
                    "currency": currency
                },
                "description": description,
                "custom": str(uuid.uuid4())[:8]
            }],
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            }
        })

        if payment.create():
            approval_url = [link.href for link in payment.links if link.rel == "approval_url"][0]
            return approval_url
        else:
            # Handle any PayPal errors here
            return None

@csrf_exempt
def paypal_webhook(request):
    if request.method == "POST":
        event_types = {
            "PAYMENT.SALE.COMPLETED": "sale.completed",
            "PAYMENT.SALE.PENDING": "sale.pending",
            "PAYMENT.SALE.DENIED": "sale.denied",
            "PAYMENT.SALE.REFUNDED": "sale.refunded",
            "PAYMENT.SALE.REVERSED": "sale.reversed",
            "PAYMENT.SALE.CANCELED": "sale.canceled"
        }

        request_data = request.body.decode("utf-8")
