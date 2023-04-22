import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payments.models import PaymentGateway
from account.fund_exception import GatewayModuleNotFound, GatewayNotConfigured, InvalidData
from payments.checkout_card import CreditCard


class StripeClientConfig:
    display_name = "stripe"
    currency = "usd"

    def __init__(self, request):
        self.merchant = request.merchant
        # Load the Stripe keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(name=self.display_name, subscription=True, status=True)
            self.stripe_secret_key = payment_gateway.secret_key
            self.stripe_public_key = payment_gateway.public_key
            self.stripe_webhook_key = payment_gateway.webhook_key
            self.stripe_subscription_price_id = payment_gateway.subscription_price_id
            stripe.api_key = self.stripe_secret_key
        except PaymentGateway.DoesNotExist:
            raise GatewayModuleNotFound("The '%s' gateway is not available." % self.display_name)


    def create_checkout(self, merchant, amount, credit_card):

        if merchant is None:
            raise InvalidData("Error occured on our side. Please try in few time")
        
        card = {
            'object': 'card',
            'number': credit_card.number,
            'exp_month': credit_card.month,
            'exp_year': credit_card.year,
            'cvc': credit_card.verification_value
        }
        
        try:
            response = stripe.Charge.create(
                name=self.merchant.get_full_name(),
                email=merchant.merchant.email,
                amount=int(amount * 100),
                currency= self.currency,
                source=card
            )

        except (stripe.error.StripeError, stripe.CardError, stripe.InvalidRequestError) as e:
            raise InvalidData(f"Error! {e}")

        return {'status': 'SUCCESS', 'response': response}
    
         
    def create_recurrent(self, credit_card, package, interval="month"):
        # validate interval for "month" or "annual"

        if self.merchant is None:
            raise InvalidData("Invalid request")
        
        card = {
            'object': 'card',
            'number': credit_card['number'],
            'exp_month': credit_card['month'],
            'exp_year': credit_card['year'],
            'cvc': credit_card['cvv']
        }
        try:
            # Create customer in stripe vault for future auto-charges
            customer = stripe.Customer.create(
                name=self.merchant.merchant.get_full_name(),
                email=self.merchant.merchant.email,
                amount=int(credit_card['amount'] * 100),
                currency= self.currency,
                source=card,
                plan=package
            )
            # Create a subscription for the customer
            response = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    "price_data": {
                        "currency": self.currency,
                        "unit_amount": credit_card.amount,
                        "product_data": {
                            'name': 'payment for subscription',
                        },
                    },
                    "quantity": 1,
                }],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                billing_cycle_anchor="now",
                metadata={"client_reference_id":self.merchant.id},
                trial_period_days=30, # must be integer like 7 for 7 days
                default_payment_method_types=["card"],
                proration_behavior="create_prorations",
                interval=interval
            )

        # except (stripe.CardError) as e:
        #     raise InvalidData(f"Error! {e}")
        # except (stripe.InvalidRequestError) as e:
        #     raise InvalidData(f"Error! {e}")
        except (stripe.error.StripeError) as e:
            raise InvalidData(f"Error! {e}")

        return {'status': 'SUCCESS', 'response': response}


    # Store this in stripe vault for the purpose of refund
    # def store(self, credit_card, options=None):
    #     card = credit_card
    #     if isinstance(credit_card, CreditCard):
    #         if not self.validate_card(credit_card):
    #             raise InvalidCard("Invalid Card")
    #         card = {
    #             'number': credit_card.number,
    #             'exp_month': credit_card.month,
    #             'exp_year': credit_card.year,
    #             'cvc': credit_card.verification_value
    #             }
    #     try:


    # def unstore(self, identification, options=None):
    #     try:
    #         customer = self.stripe.Customer.retrieve(identification)
    #         response = customer.delete()
    #         transaction_was_successful.send(sender=self,
    #                                           type="unstore",
    #                                           response=response)
    #         return {"status": "SUCCESS", "response": response}
    #     except self.stripe.InvalidRequestError as error:
    #         transaction_was_unsuccessful.send(sender=self,
    #                                           type="unstore",
    #                                           response=error)
    #         return {"status": "FAILURE", "response": error}


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
           
