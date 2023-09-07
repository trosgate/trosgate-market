import razorpay
from django.contrib.sites.models import Site
from payments.models import MerchantAPIs
from account.fund_exception import InvalidData
from general_settings.currency import get_base_currency_code



class RazorpayClientConfig:
    currency_notation = 100

    def __init__(self):
        self.name = 'razorpay'
        self.mysite = Site.objects.get_current()
        self.site = self.mysite.merchant
        self.currency = self.default_currency() #razorpay accept currency in uppercase

        self.razorpay_key_id = self.razorpay_key_id()
        self.razorpay_key_secret = self.razorpay_key_secret()

        self.razorpay = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))


    def get_payment_gateway(self):
        merchant = MerchantAPIs.objects.filter(merchant=self.site, razorpay_active=True).first()
        return merchant

    def default_currency(self):
        currency = self.site.merchant.country.currency
        return currency if currency else 'INR'

    def razorpay_key_id(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.razorpay_public_key_id
        return None


    def razorpay_key_secret(self):
        gateway = self.get_payment_gateway()
        if gateway:
            return gateway.razorpay_secret_key_id
        return None


    def create_order(self, amount):
        try:
            data = {
                'amount': int(amount * self.currency_notation),
                'currency': self.currency,
                'notes': {
                    'Freelancer': f'Hire of freelancer on {self.site}',
                    'Total Price': 'The total amount may change with discount'
                },
            }
            order = self.razorpay.order.create(data=data)
            return order['id']
        except Exception as e:
            raise InvalidData(f"Error! {e}")


    def capture_payment(self, payment_id, amount):
        try:
            payment = self.razorpay.payment.fetch(payment_id)
            if payment['status'] == 'captured':
                # The payment has already been captured
                return True

            # Capture the payment
            self.razorpay.payment.capture(payment_id, amount=int(amount * self.currency_notation))
            return True
        except Exception as e:
            raise InvalidData(f"Error! {e}")


    def refund(self, payment_id, amount):
        try:
            refund = self.razorpay.payment.refund(payment_id, amount=int(amount * self.currency_notation))
            return refund['id']
        except Exception as e:
            raise InvalidData(f"Error! {e}")
