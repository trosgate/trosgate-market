from .models import PaymentAccount, PaymentRequest, AdminCredit
from django import forms
from account.fund_exception import FundException
from notification.mailer import send_credit_to_team, send_withdrawal_marked_failed_email
from django.utils.translation import gettext_lazy as _


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


























































