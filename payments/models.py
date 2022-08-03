from django.db import models, transaction as db_transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .payday import get_payday_deadline
from django_cryptography.fields import encrypt
from account.fund_exception import FundException


class PaymentAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='paymentaccount', on_delete=models.PROTECT,)
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


    @classmethod
    def payment_mode(cls, user, paypal:None, stripe:None, flutterwave:None, razorpay:None):
        with db_transaction.atomic():
            account = cls.objects.select_for_update().get(pk=user.id)

            if paypal != '':
                account.paypal = paypal
            if stripe != '':
                account.stripe = stripe
            if flutterwave != '':
                account.flutterwave = flutterwave
            if razorpay != '':
                account.razorpay = razorpay

            account.save(update_fields=['paypal', 'stripe', 'flutterwave', 'razorpay'])
            return account


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
        ordering = ['-created_at']
        verbose_name = 'Payment Request'
        verbose_name_plural = 'Payment Request'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


    @classmethod
    def create(cls, user, team, amount, gateway):
        return cls.objects.create(user=user, team=team, amount=amount, gateway=gateway)


class AdminCredit(models.Model): 
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admincreditor', on_delete=models.PROTECT,)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creditreceiver', on_delete=models.PROTECT,)
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='admincreditteam', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(_("Amount"), default=0,)
    comment = models.TextField(_("Credit Comment"), max_length=200)
    reference = models.CharField(_("STAN"), max_length=200, blank=True, help_text=_("STAN means System Audit Trail Number"),)
    created_at = models.DateTimeField(_("Started On"), auto_now_add=True,)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admin Credit'
        verbose_name_plural = 'Admin Credits'

    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name}'

    @classmethod
    def create(cls, sender, receiver, team, amount, comment, created_at):        
        credit = cls.objects.create(sender=sender, receiver=receiver, team=team, amount=amount, comment=comment, created_at=created_at)
        stan = f'{credit.pk}'.zfill(6)
        credit.reference = f'STAN-{stan}'
        credit.save()
        return credit

    # @classmethod
    # def confirm_and_mark_paid(cls, pk:int):
    #     with db_transaction.atomic():
    #         payout = cls.objects.select_for_update().get(pk=pk)
    #         if payout.status != 'pending':
    #             raise FundException(_("Only pending transaction can be marked"))
    #         payout.status = 'paid'
    #         payout.save()
    #     return payout





















