from .models import PaymentAccount
from django import forms

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = PaymentAccount
        fields = ['paypal', 'stripe', 'flutterwave', 'razorpay']

    def __init__(self, *args, **kwargs):
        super(PaymentAccountForm, self).__init__(*args, **kwargs)

        self.fields['paypal'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center'})
        self.fields['stripe'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center'})
        self.fields['flutterwave'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center'})
        self.fields['razorpay'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center'})


