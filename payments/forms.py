from .models import PaymentGateway, PaymentAccount, PaymentRequest, AdminCredit
from django import forms
from account.fund_exception import FundException
from notification.mailer import send_credit_to_team, send_withdrawal_marked_failed_email
from django.utils.translation import gettext_lazy as _
from .models import PaymentGateway, MerchantAPIs
import datetime
from .checkout_card import CreditCard



class StripeMerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantAPIs
        fields = [
            # Stripe
            'stripe_public_key', 'stripe_secret_key', 'stripe_webhook_key', 
            'stripe_subscription_price_id',  
        ]
        
    def __init__(self, *args, **kwargs):
        super(StripeMerchantForm, self).__init__(*args, **kwargs)
   
        # Flutterwave
        self.fields['stripe_public_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_secret_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_webhook_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_subscription_price_id'].widget.attrs.update(
            {'class': 'form-control'})


class PayPalMerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantAPIs
        fields = [
            # Stripe
            'paypal_public_key', 'paypal_secret_key', 
            'paypal_subscription_price_id', 'sandbox',  
        ]
        
    def __init__(self, *args, **kwargs):
        super(PayPalMerchantForm, self).__init__(*args, **kwargs)

        # Flutterwave
        self.fields['paypal_public_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paypal_secret_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paypal_subscription_price_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['sandbox'].widget.attrs.update(
            {'class': 'form-control'})


class PaystackMerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantAPIs
        fields = [
            # Stripe
            'paystack_public_key', 'paystack_secret_key', 
            'paystack_subscription_price_id', 'paystack_active',  
        ]
        
    def __init__(self, *args, **kwargs):
        super(PaystackMerchantForm, self).__init__(*args, **kwargs)

        # Flutterwave
        self.fields['paystack_public_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paystack_secret_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paystack_subscription_price_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paystack_active'].widget.attrs.update(
            {'class': 'form-control'})


class FlutterwaveMerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantAPIs
        fields = [
            # Stripe
            'flutterwave_public_key', 'flutterwave_secret_key', 
            'flutterwave_subscription_price_id', 'flutterwave_active',  
        ] #19805
        
    def __init__(self, *args, **kwargs):
        super(FlutterwaveMerchantForm, self).__init__(*args, **kwargs)

        # Flutterwave
        self.fields['flutterwave_public_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_secret_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_subscription_price_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_active'].widget.attrs.update(
            {'class': 'form-control'})


class RazorpayMerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantAPIs
        fields = [
            # Stripe
            'razorpay_public_key_id', 'razorpay_secret_key_id', 
            'razorpay_subscription_price_id', 'sandbox',  
        ]
        
    def __init__(self, *args, **kwargs):
        super(RazorpayMerchantForm, self).__init__(*args, **kwargs)

        # Flutterwave
        self.fields['razorpay_public_key_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['razorpay_secret_key_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['razorpay_subscription_price_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['sandbox'].widget.attrs.update(
            {'class': 'form-control'})


class MTNMerchantForm(forms.ModelForm):
    class Meta:
        model = MerchantAPIs
        fields = [
            # Stripe
            'mtn_api_user_id', 'mtn_api_key', 
            'mtn_subscription_key', 'mtn_callback_url', 'sandbox',  
        ]
        
    def __init__(self, *args, **kwargs):
        super(MTNMerchantForm, self).__init__(*args, **kwargs)

        # Flutterwave
        self.fields['mtn_api_user_id'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['mtn_api_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['mtn_subscription_key'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['mtn_callback_url'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['sandbox'].widget.attrs.update(
            {'class': 'form-control'})


CARD_TYPES = [
    ('', ''),
    ('visa', 'Visa'),
    ('master', 'Master'),
    ('discover', 'Discover'),
    ('american_express', 'American Express'),
]

today = datetime.date.today()
MONTH_CHOICES = [(m, datetime.date(today.year, m, 1).strftime('%b')) for m in range(1, 13)]
current_year = datetime.datetime.now().year
YEAR_CHOICES = [(year, str(year)) for year in range(current_year, current_year + 21)]


class StripeCardCardForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=True, label='Expiry Month*')
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label='Expiry Year*')
    number = forms.CharField(required=True, label='Card Number*')
    cvc = forms.CharField(required=True, label='Card cvc*')
    # amount = forms.IntegerField(required=True)

    def clean_number(self):
        number = self.cleaned_data['number'].strip()
        if not number: # or number.isspace():
            raise forms.ValidationError('Missing card number')
        return number
    
    def clean_cvc(self):
        cvc = self.cleaned_data['cvc'].strip()
        if not cvc:
            raise forms.ValidationError('Missing card cvc')
        return cvc
    
    def clean(self):
        data = self.cleaned_data
        credit_card = CreditCard(**data)
        if not credit_card.is_valid():
            raise forms.ValidationError('Payment card validation failed')
        return data
    
    def __init__(self, *args, **kwargs):
        super(StripeCardCardForm, self).__init__(*args, **kwargs)

        # self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['cvc'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'custom-select'
        self.fields['year'].widget.attrs['style'] = 'height: 50px;'
        self.fields['month'].widget.attrs['class'] = 'custom-select'
        self.fields['month'].widget.attrs['style'] = 'height: 50px;'
        

class CreditCardForm(forms.Form):
    first_name = forms.CharField(required=True, label='First name*')
    last_name = forms.CharField(required=True, label='First name*')
    package = forms.CharField(required=True)
    # amount = forms.IntegerField(required=True)
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=True, label='Expiry Month*')
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label='Expiry Year*')
    number = forms.CharField(required=True, label='Card Number*')
    cvc = forms.CharField(required=True, label='Card cvc*')

    def clean_number(self):
        number = self.cleaned_data['number'].strip()
        if not number or number.isspace():
            raise forms.ValidationError('Missing card number')
        return number
    
    def clean_cvc(self):
        cvc = self.cleaned_data['cvc'].strip()
        if not cvc:
            raise forms.ValidationError('Missing card cvc')
        return cvc
    
    def clean(self):
        data = self.cleaned_data
        credit_card = CreditCard(**data)
        if not credit_card.is_valid():
            raise forms.ValidationError('Payment card validation failed')
        return data
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(CreditCardForm, self).__init__(
            *args, 
            initial={
            'first_name':request.user.first_name,
            'last_name':request.user.last_name},
            **kwargs
        )
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['cvc'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'custom-select'
        self.fields['year'].widget.attrs['style'] = 'height: 50px;'
        self.fields['month'].widget.attrs['class'] = 'custom-select'
        self.fields['month'].widget.attrs['style'] = 'height: 50px;'
        

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = PaymentAccount
        fields = [
            'primary_account_type',
            # Flutterwave
            'flutterwave_country', 'flutterwave_type', 'flutterwave_bank', 'flutterwave_bearer',
            'flutterwave_account', 'flutterwave_swift_iban', 'flutterwave_extra_info',
            # Paypal
            'paypal_account', 'paypal_bearer', 'paypal_country',
            # Stripe
            'stripe_country', 'stripe_bank', 'stripe_account', 'stripe_routing',
            'stripe_swift_iban', 'stripe_bearer', 'stripe_extra_info',
            # Razorpay
            'razorpay_bearer', 'razorpay_upi','razorpay_country',    
            ]

    def __init__(self, *args, **kwargs):
        super(PaymentAccountForm, self).__init__(*args, **kwargs)
        self.fields['primary_account_type'].queryset = PaymentGateway.objects.filter(status=True).exclude(name='Balance')
        # Flutterwave
        self.fields['primary_account_type'].widget.attrs.update(
            {'class': 'form-control col-md-6'})
        self.fields['flutterwave_country'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_type'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_bank'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_bearer'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_account'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_swift_iban'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['flutterwave_extra_info'].widget.attrs.update(
            {'class': 'form-control'})
        # PayPal
        self.fields['paypal_account'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paypal_bearer'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['paypal_country'].widget.attrs.update(
            {'class': 'form-control'})
        
        # Stripe
        self.fields['stripe_country'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_bank'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_account'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_routing'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_swift_iban'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_bearer'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_bearer'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['stripe_extra_info'].widget.attrs.update(
            {'class': 'form-control'})
        # Razorpay           
        self.fields['razorpay_bearer'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['razorpay_upi'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['razorpay_country'].widget.attrs.update(
            {'class': 'form-control'})


class BaseMemoForm(forms.Form):
    APPROVED = 'approve'
    STATUS_CHOICES = (
        (APPROVED, _('Approve')),
    )    
    status = forms.ChoiceField(required=True, choices=STATUS_CHOICES, label="Submit to Approve")
    
    def form_action(self, account, user):

        if account == '':
            raise FundException(_("Bad request. Try again later"))
        if user == '':
            raise FundException(_("Bad request. Try again later"))

    def save(self, account, user):
        try:
            action = self.form_action(account, user)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)           
            raise
            
        return account, action


class AdminApproveForm(BaseMemoForm):

    def form_action(self, account, user):
        return AdminCredit.approve_credit_memo(
            pk=account.id,
            user=user,
        )


class PaymentChallengeForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}), help_text='We will take care of Salutation and the details like amount, team, username. Go straight to the point and describe error and what to do. Ex, Payment company declined payment, Account details provided are invalid etc', required=True)
    send_email = forms.BooleanField(required=True,)

    def form_action(self, payout, message):
        
        if message == '':
            raise FundException(_("Message is required"))

        if payout == '':
            raise FundException(_("Bad request. Try again later"))

    def save(self, payout, message):
        try:
            action = self.form_action(payout, message)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)           
            raise
        
        return action

    field_order = ('message', 'send_email',)

    def form_action(self, payout, message):
        return PaymentRequest.payment_declined(
            pk=payout,
            message = self.cleaned_data['message'],
        )


























































