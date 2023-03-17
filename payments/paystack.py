import paystack
from django.conf import settings
from payments.models import PaymentGateway

class PaystackCheckout:
    def __init__(self):
        self.name = "paystack"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
            ("paystack", "Paystack")
        )
        # Load the Paystack keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="paystack")
            self.paystack_secret_key = payment_gateway.secret_key
            self.paystack_public_key = payment_gateway.public_key
            paystack.secret_key = self.paystack_secret_key
        except PaymentGateway.DoesNotExist:
            raise Exception("Paystack payment gateway not configured")

    def create_checkout(self, charge):
        # Generate unique transaction reference
        tx_ref = f"{self.name}_{charge.id}"
        
        # Create payment request
        paystack_response = paystack.Transaction.initialize(
            reference=tx_ref,
            amount=charge.amount,
            email=charge.email,
            callback_url=charge.callback_url,
        )
        
        # Return payment URL for redirection
        return paystack_response['data']['authorization_url']
        
    def create_subscription(self, subscription):
        # Generate unique transaction reference
        tx_ref = f"{self.name}_{subscription.id}"
        
        # Create subscription request
        paystack_response = paystack.Subscription.create(
            customer=subscription.customer,
            plan=subscription.plan,
            email=subscription.email,
            reference=tx_ref,
        )
        
        # Check if subscription was successful
        if paystack_response['status']:
            # Return subscription ID for future use
            return paystack_response['data']['subscription_code']
        else:
            # Raise an exception with error message
            raise Exception(paystack_response['message'])
        
    def validate_request(self, request):
        # Validate Paystack webhook request
        signature = request.headers.get('X-Paystack-Signature')
        paystack_response = paystack.utils.webhook.verify(
            request.body, 
            signature, 
            self.paystack_secret_key
        )
        
        # Check if request was successful
        if paystack_response['status']:
            # Return Paystack response data
            return paystack_response['data']
        else:
            # Raise an exception with error message
            raise Exception(paystack_response['message'])
