from django.db import models, transaction as db_transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .payday import get_payday_deadline
from django_cryptography.fields import encrypt
from account.fund_exception import FundException
from notification.mailer import send_credit_to_team, send_marked_paid_in_bulk_email, send_withdrawal_marked_failed_email
from account.models import Customer
from teams.models import Team


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paymentrequest', on_delete=models.PROTECT,)
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='paymentrequesterteam', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(_("Amount"), default=0,)
    status = models.BooleanField(_("Action Type"), choices=((False, 'Pending'), (True, 'Paid')), default=False)
    gateway = models.CharField(_("Payment Account"), max_length=50)
    message = models.TextField(_("Payment Error Message"), max_length=500, null=True, blank=True)
    payday = models.DateTimeField(_("Payment Due"), null=True, blank=True)
    created_at = models.DateTimeField(_("Requested On"), auto_now_add=True,)
    modified_on = models.DateTimeField(auto_now=True,)
    reference = models.CharField(_("Ref Number"), max_length=15, blank=True, help_text=_("This is a unique number assigned for audit purposes"),)

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
        payout =  cls.objects.create(user=user, team=team, amount=amount, gateway=gateway)
        stan = f'{payout.pk}'.zfill(8)
        payout.reference = f'REQ-{stan}'
        payout.save()
        return payout        
    
    
    @classmethod
    def mark_paid(cls, pk:int):
        with db_transaction.atomic():
            payout = cls.objects.select_for_update().get(pk=pk)
            if payout.status != False:
                raise Exception(_("The request must be in Pending state before you can mark as paid"))
            payout.status = True
            payout.save()

            db_transaction.on_commit(lambda: send_marked_paid_in_bulk_email(payout))

        return payout


    @classmethod
    def payment_declined(cls, pk:int, message):
        with db_transaction.atomic():
            payout = cls.objects.select_for_update().get(pk=pk)
            if payout.status != False:
                raise Exception(_("The request must be in Pending state before you can mark as paid"))
            
            if message == '':
                raise Exception(_("message is required"))

            message_count = len(message)
            if len(message) > 500:
                raise Exception(_(f"message exceeds 500 words required. You entered {message_count} words"))
            
            payout.message = message
            payout.save(update_fields=['message'])

            db_transaction.on_commit(lambda: send_withdrawal_marked_failed_email(payout))

        return payout


class AdminCredit(models.Model):
    INITIATED = 'initiated'
    APPROVED = 'approved'
    STATUS_CHOICES = (
        (INITIATED, _('Initiated')),
        (APPROVED, _('Approved')),
    )     
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admincreditor', on_delete=models.PROTECT,)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creditreceiver', on_delete=models.PROTECT,)
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='admincreditteam', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(_("Amount"), default=0,)
    comment = models.TextField(_("Credit Comment"), max_length=200)
    reference = models.CharField(_("STAN"), max_length=200, blank=True, help_text=_("STAN means System Audit Trail Number"),)
    created_at = models.DateTimeField(_("Started On"), auto_now_add=True,)
    status = models.CharField(_("Status"), choices=STATUS_CHOICES, default=INITIATED, max_length=20)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Credit Memo'
        verbose_name_plural = 'Credit Memos'

    def __str__(self):
        return f'{self.sender.first_name} {self.sender.last_name}'

    @classmethod
    def create(cls, sender, receiver, team, amount, comment, created_at):        
        credit = cls.objects.create(sender=sender, receiver=receiver, team=team, amount=amount, comment=comment, created_at=created_at)
        stan = f'{credit.pk}'.zfill(6)
        credit.reference = f'STAN-{stan}'
        credit.save()
        return credit
 
    @classmethod
    def approve_credit_memo(cls, pk, user):
        with db_transaction.atomic():
            credit_account = cls.objects.select_for_update().get(pk=pk)
            super_admin_user = Customer.objects.select_for_update().filter(is_superuser=True).first()
            owner_active_team = Team.objects.select_for_update().filter(created_by=credit_account.team.created_by, status=Team.ACTIVE).first()
            account = Customer.objects.select_for_update().get(pk=credit_account.team.created_by.id).fundtransferuser #I am accessing from customer to avoid circular import
            
            if credit_account.status != 'initiated':
                raise FundException(_("account must be in initiated state to approve"))

            if user.is_superuser == False:
                raise FundException(_("All approvals must be performed by the SuperAdmin Only"))

            if super_admin_user != user:
                raise FundException(_("This is not your assigned task"))

            credit_account.status = 'approved'
            credit_account.save(update_fields=['status'])

            account.available_balance += int(credit_account.amount)
            account.save(update_fields=['available_balance'])

            owner_active_team.team_balance += int(credit_account.amount)
            owner_active_team.save(update_fields=['team_balance'])

            db_transaction.on_commit(lambda: send_credit_to_team(credit_account))

        return account, super_admin_user, owner_active_team
















