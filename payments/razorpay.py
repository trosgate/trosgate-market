import uuid
import razorpay

class RazorpayCheckout:
    def __init__(self):
        self.name = "razorpay"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
        )
        self.key_id = ""
        self.key_secret = ""

        # Load the Razorpay keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="razorpay")
            self.key_id = payment_gateway.public_key
            self.key_secret = payment_gateway.secret_key
        except PaymentGateway.DoesNotExist:
            pass

    def create_checkout(self, amount, currency="INR", description="", customer_email=None, success_url=None, cancel_url=None):
        client = razorpay.Client(auth=(self.key_id, self.key_secret))

        order_id = str(uuid.uuid4())[:20]

        payload = {
            "amount": amount * 100, # Amount in paise
            "currency": currency,
            "receipt": order_id,
            "payment_capture": "1",
            "notes": {
                "description": description,
            },
            "customer": {
                "email": customer_email,
            }
        }

        response = client.order.create(data=payload)

        if response.get("id") is not None:
            order = response.get("id")
            return {
                "order_id": order_id,
                "order": order,
                "key_id": self.key_id,
                "amount": amount,
                "currency": currency,
                "name": description,
                "description": description,
                "prefill": {
                    "name": customer_email,
                    "email": customer_email,
                },
                "handler": success_url,
                "theme": {
                    "color": "#F37254",
                },
            }
        else:
            # Handle any Razorpay checkout creation errors here
            return f"Error creating Razorpay checkout: {response.text}"
