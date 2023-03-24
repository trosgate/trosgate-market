import paypalrestsdk
from payments.models import PaymentGateway

class PaypalCheckout:
    def __init__(self):
        self.name = "paypal"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
        )
        # Load the PayPal credentials from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="paypal")
            self.paypal_client_id = payment_gateway.client_id
            self.paypal_secret_key = payment_gateway.secret_key
            paypalrestsdk.configure({
                "mode": "sandbox", # Set to "live" for production
                "client_id": self.paypal_client_id,
                "client_secret": self.paypal_secret_key
            })
        except PaymentGateway.DoesNotExist:
            raise Exception("PayPal payment gateway not found in the database")
        
    def create_checkout(self, amount, currency="USD", description="", success_url=None, cancel_url=None):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": currency,
                },
                "description": description,
            }],
            "redirect_urls": {
                "return_url": success_url,
                "cancel_url": cancel_url,
            },
        })
        if payment.create():
            # Save the PayPal payment ID in the session
            payment_id = payment.id
            request.session["paypal_payment_id"] = payment_id

            # Extract the PayPal payment approval URL from the payment object
            for link in payment.links:
                if link.method == "REDIRECT":
                    approval_url = str(link.href)
                    return {"url": approval_url}
        else:
            # Handle any PayPal errors here
            return None

        # if payment.create():
        #     for link in payment.links:
        #         if link.rel == "approval_url":
        #             return link.href
        # else:
        #     # Handle any PayPal errors here
        #     return None
            
    def create_recurrent(self, amount, currency="USD", description="", customer_email=None, success_url=None, cancel_url=None, interval="MONTH"):
            plan = paypalrestsdk.Plan({
                "name": description,
                "description": description,
                "type": "INFINITE",
                "payment_definitions": [{
                    "name": "Regular payment definition",
                    "type": "REGULAR",
                    "frequency_interval": 1,
                    "frequency": interval,
                    "amount": {
                        "value": str(amount),
                        "currency": currency
                    },
                    "cycles": "0",
                    "charge_models": [{
                        "type": "SHIPPING",
                        "amount": {
                            "value": "0",
                            "currency": currency
                        }
                    }]
                }],
                "merchant_preferences": {
                    "cancel_url": cancel_url,
                    "return_url": success_url,
                    "auto_bill_amount": "YES",
                    "initial_fail_amount_action": "CONTINUE",
                    "max_fail_attempts": "0"
                }
            })
            if plan.create():
                agreement = paypalrestsdk.Agreement({
                    "name": description,
                    "description": description,
                    "start_date": "2023-04-01T00:00:00Z",
                    "plan": {
                        "id": plan.id
                    },
                    "payer": {
                        "payment_method": "paypal",
                    },
                    "shipping_address": {
                        "line1": "1234 Elm Street",
                        "city": "San Jose",
                        "state": "CA",
                        "postal_code": "95131",
                        "country_code": "US"
                    }
                })
                if agreement.create():
                    for link in agreement.links:
                        if link.rel == "approval_url":
                            return link.href
                else:
                    # Handle any PayPal agreement creation errors here
                    return f"Error creating PayPal agreement: {agreement.error}"
            else:
                # Handle any PayPal plan creation errors here
                return f"Error creating PayPal plan: {plan.error}"

    def webhook(self, request):
        # Verify the webhook request
        try:
            event = paypalrestsdk.WebhookEvent(request.body, request.META["HTTP_PAYPAL_SIGNATURE"])
        except ValueError:
            # Invalid payload
            return HttpResponse(status=400)
        except paypalrestsdk.exceptions.UnauthorizedAccess:
            # Invalid signature
            return HttpResponse(status=401)

        # Handle the event based on its type
        if event.event_type == "PAYMENT.SALE.COMPLETED":
            sale = paypalrestsdk.Sale.find(event.resource["parent_payment"])
            # Process the completed sale here
            return HttpResponse(status=200)
        elif event.event_type == "PAYMENT.SALE.DENIED":
            # Handle the denied sale here
            return HttpResponse(status=200)
        else:
            # Ignore unknown events
            return HttpResponse(status=200)