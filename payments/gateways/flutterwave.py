import uuid
import requests

class FlutterwaveCheckout:
    def __init__(self):
        self.name = "flutterwave"
        self.type_choices = (
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("razorpay", "Razorpay"),
            ("flutterwave", "Flutterwave"),
        )
        self.public_key = ""
        self.secret_key = ""

        # Load the Flutterwave keys from the database
        try:
            payment_gateway = PaymentGateway.objects.get(status="flutterwave")
            self.public_key = payment_gateway.public_key
            self.secret_key = payment_gateway.secret_key
        except PaymentGateway.DoesNotExist:
            pass

    def create_checkout(self, amount, currency="NGN", description="", customer_email=None, success_url=None, cancel_url=None):
        url = "https://api.flutterwave.com/v3/payments"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_key}"
        }

        tx_ref = str(uuid.uuid4())[:20]

        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "redirect_url": success_url,
            "payment_options": "card",
            "meta": {
                "customer_email": customer_email,
            },
            "customer": {
                "email": customer_email,
            },
            "customizations": {
                "title": description,
                "description": description,
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data["data"]["link"]
        else:
            # Handle any Flutterwave checkout creation errors here
            return f"Error creating Flutterwave checkout: {response.text}"
        
    def create_subscription(self, amount, currency="NGN", description="", customer_email=None, interval="monthly", duration=0):
        url = "https://api.flutterwave.com/v3/subscriptions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_key}"
        }

        payload = {
            "plan_id": None,
            "amount": amount,
            "currency": currency,
            "start_date": None,
            "interval": interval,
            "duration": duration,
            "name": description,
            "description": description,
            "payment_options": "card",
            "meta": {
                "customer_email": customer_email,
            },
            "customer": {
                "email": customer_email,
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data["data"]["link"]
        else:
            # Handle any Flutterwave subscription creation errors here
            return f"Error creating Flutterwave subscription: {response.text}"
