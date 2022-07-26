from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .payday import get_payday_deadline
from django_cryptography.fields import encrypt


class PaymentAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paymentaccount', on_delete=models.PROTECT,)
    paypal = encrypt(models.CharField(_("PayPal Account"), max_length=100, help_text=_(
        'Paypal Account to receive payment'), null=True, blank=True))
    stripe = encrypt(models.CharField(_("Stripe Account"), max_length=100, help_text=_(
        'Stripe Account to receive payment'), null=True, blank=True))
    flutterwave = encrypt(models.CharField(_("Flutterwave Account"), max_length=100, help_text=_(
        'Flutterwave Account to receive payment'), null=True, blank=True))
    razorpay = encrypt(models.CharField(_("Razorpay Account"), max_length=100, help_text=_(
        'Razorpay Account to receive payment'), null=True, blank=True))
    created_at = models.DateTimeField(_("Started On"), auto_now_add=True,)
    modified_on = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'Payment Account'
        verbose_name_plural = 'Payment Account'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class PaymentRequest(models.Model):
    # Status Choices
    PENDING = 'pending'
    PAID = 'paid'
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (PAID, _("Paid")),
    )    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paymentrequest', on_delete=models.PROTECT,)
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='paymentrequesterteam', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(_("Amount"), default=0,)
    status_choice = models.CharField(_("Action Type"), max_length=50, choices=STATUS_CHOICES, default=PENDING)
    gateway = models.CharField(_("Payment Account"), max_length=50)
    payday = models.DateTimeField(_("PayDay By"), null=True, blank=True)
    created_at = models.DateTimeField(_("Started On"), auto_now_add=True,)
    modified_on = models.DateTimeField(auto_now=True,)

    def save(self, *args, **kwargs):
        if self.payday is None:
            self.payday = get_payday_deadline()       
        super(PaymentRequest, self).save(*args, **kwargs) 

    class Meta:
        verbose_name = 'Payment Request'
        verbose_name_plural = 'Payment Request'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


    @classmethod
    def create(cls, user, team, amount, gateway):
        return cls.objects.create(user=user, team=team, amount=amount, gateway=gateway)






















