import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payments.models import PaymentGateway, StripeMerchant
from account.fund_exception import GatewayModuleNotFound, GatewayNotConfigured, InvalidData


class StripeClientConfig:
    display_name = "Stripe"

    def __init__(self, request):
        self.merchant = request.merchant
        # Load the Stripe keys from the database
        try:
            gateway = PaymentGateway.objects.get(name=self.display_name, status='active')
        except PaymentGateway.DoesNotExist:
            raise GatewayModuleNotFound("The '%s' gateway is not available." % self.display_name)

        try:
            active_gateway = gateway
            payment_gateway=StripeMerchant.objects.get(merchant=self.merchant, gateway=active_gateway, status=self.name)
            self.stripe_secret_key = payment_gateway.stripe_secret_key
            self.stripe_public_key = payment_gateway.stripe_public_key
            self.stripe_webhook_key = payment_gateway.stripe_webhook_key
            self.stripe_subscription_price_id = payment_gateway.stripe_subscription_price_id
            stripe.api_key = self.stripe_secret_key
        
        except PaymentGateway.DoesNotExist:
            raise GatewayNotConfigured("The '%s' gateway is not configured." % self.display_name)

        
    def create_checkout(self, amount, currency="usd", customer_email=None, success_url=None, cancel_url=None):
        try:
            session = stripe.checkout.Session.create(
                metadata = {'mode':'payment', 'customer_email':customer_email},
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount* 100,
                        "product_data": {
                            'name': 'Hiring of freelancer',
                        },
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return session.id
        except stripe.error.StripeError as e:
            # Handle any Stripe errors here
            return None

      
    def create_recurrent(self, amount, expiry_period, currency="usd", merchant="", customer_email=None, success_url=None, cancel_url=None, interval="month"):
        try:
            customer = stripe.Customer.create(email=customer_email)
            subscription = stripe.Subscription.create(
                customer=customer.id,
                plan=plan_id
                items=[{
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            'name': 'payment for subscription',
                        },
                    },
                    "quantity": 1,
                }],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                billing_cycle_anchor="now",
                cancel_url=cancel_url,
                success_url=success_url,
                metadata={"client_reference_id":merchant},
                trial_period_days=expiry_period, # must be integer like 7 for 7 days
                default_payment_method_types=["card"],
                proration_behavior="create_prorations",
                interval=interval
            )
            return subscription.id
        except stripe.error.StripeError as e:
            # Handle any Stripe errors here
            return None

    
    @csrf_exempt
    def handle_webhook(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = 'your_endpoint_secret'  # replace with your webhook endpoint secret
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Handle completed checkout session
            # ...
        elif event['type'] == 'customer.subscription.created':
            subscription = event['data']['object']
            # Handle created subscription
           
