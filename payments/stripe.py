import stripe
from payments.models import PaymentGateway

class StripeCheckout:
    def __init__(self):
        self.name = "stripe"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
        )
        # Load the Stripe keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="stripe")
            self.stripe_secret_key = payment_gateway.secret_key
            self.stripe_public_key = payment_gateway.public_key
            stripe.api_key = self.stripe_secret_key
        except PaymentGateway.DoesNotExist:
            raise Exception("Stripe payment gateway not found in the database")
        
    def create_checkout(self, amount, currency="usd", description="", customer_email=None, success_url=None, cancel_url=None):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            "name": description,
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
        
    def create_recurrent(self, amount, currency="usd", description="", customer_email=None, success_url=None, cancel_url=None, interval="month"):
        try:
            customer = stripe.Customer.create(email=customer_email)
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            "name": description,
                        },
                    },
                    "quantity": 1,
                }],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                billing_cycle_anchor="now",
                cancel_url=cancel_url,
                success_url=success_url,
                metadata={"description": description},
                trial_period_days=7,
                default_payment_method_types=["card"],
                proration_behavior="create_prorations",
                interval=interval
            )
            return subscription.id
        except stripe.error.StripeError as e:
            # Handle any Stripe errors here
            return None
