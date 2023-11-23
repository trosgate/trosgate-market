from django.db import models, transaction as db_transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .payday import get_payday_deadline
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django_cryptography.fields import encrypt
from django.core.exceptions import ValidationError
from account.fund_exception import FundException
from notification.mailer import send_credit_to_team, send_marked_paid_in_bulk_email, send_withdrawal_marked_failed_email
from account.models import Customer,Merchant
from teams.models import Team
from merchants.models import MerchantMaster
from django.contrib.sites.models import Site
from teams.utilities import generate_unique_reference
from freelancer.models import FreelancerAccount
from django.utils import timezone
from dateutil.relativedelta import relativedelta




class PaymentAPI(models.Model): # This model stores apis for parent site
    public_key = encrypt(models.CharField(_("Puplishable Key/API Id"), max_length=255, blank=True, null=True))
    secret_key = encrypt(models.CharField(_("Secret Key/API Key"), max_length=255, blank=True, null=True))
    webhook_key = encrypt(models.CharField(
        _("API Webhook"), 
        max_length=255, 
        blank=True, 
        null=True,
        help_text=_(
        "This is mandatory for payment with Mobile money, Stripe. Optional for other gateways"),
    ))
    subscription_price_id = encrypt(models.CharField(_("Subscription Id"), max_length=255, blank=True, null=True))
    sandbox = models.BooleanField(_("Sandbox Mode"), choices=((False, 'No'), (True, 'Yes')), default=True)

    class Meta:
        verbose_name = 'Payment API'
        verbose_name_plural = 'Payment API'
        abstract = True


class PaymentGateway(PaymentAPI):
    BALANCE = 'balance'
    STRIPE = 'stripe'
    PAYPAL = 'paypal' 
    FLUTTERWAVE = 'flutterwave'
    RAZORPAY = 'razorpay'
    PAYSTACK = 'paystack'
    GATEWAY_TYPE = (
        (BALANCE, _('Balance')),
        (STRIPE, _('Stripe')),
        (PAYPAL, _('PayPal')),
        (FLUTTERWAVE, _('Flutterwave')),
        (RAZORPAY, _('Razorpay')),
        (PAYSTACK, _('Paystack')),
    )
    name = models.CharField(
        _("Payment Gateway"), 
        choices=GATEWAY_TYPE, 
        default=BALANCE, 
        max_length=20, 
        unique=True
    )
    status = models.BooleanField(
        _("Status"), 
        choices=((False, 'Inactive'), (True, 'Active')), 
        default=False
    )
    processing_fee = models.PositiveIntegerField(
        _("Processing Fee"),
        default=0, 
        help_text=_(
        "discount price must be less than actual price"), 
        validators=[MinValueValidator(0), MaxValueValidator(20000)]
    )
    ordering = models.PositiveIntegerField(
        _("Ordering"), default=1, 
        help_text=_(
        "This determines how each Gateway will appear to user eg, 1 means 1st position"), 
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    subscription = models.BooleanField(_("Merchant Payment Support"), choices=(
        (False, 'Disabled Subscription'), (True, 'Enabled Subscription')), default=False)
    
    default = models.BooleanField(_("Default"), choices=(
        (False, 'No'), (True, 'Yes')), default=True)

    def __str__(self):
        return str(self.get_name_display())

    class Meta:
        ordering = ['ordering']

    def clean(self):
        # Start amount against delta validation
        if self.subscription == True and self.public_key is None or self.subscription == True and self.public_key == '':
            raise ValidationError(
                {'public_key': _('Field required for subscription')})
        
        if self.subscription == True and self.secret_key is None or self.subscription == True and self.secret_key == '':
            raise ValidationError(
                {'secret_key': _('Field required for subscription')})
        
        if (self.name == 'stripe' and self.subscription == True) and self.webhook_key is None or self.webhook_key == '':
            raise ValidationError(
                {'webhook_key': _('Field required for subscription')})
        
        if (self.name == 'mtn_momo' and self.subscription == True) and self.webhook_key is None or self.webhook_key == '':
            raise ValidationError(
                {'webhook_key': _('Field required for subscription')})
        
        if self.subscription == True and self.subscription_price_id is None or self.subscription == True and self.subscription_price_id == '':
            raise ValidationError(
                {'subscription_price_id': _('Field required for subscription')})
                 
        return super().clean()


class MerchantAPIs(models.Model):
    # This model stores apis for parent site
    merchant = models.OneToOneField('account.Merchant', verbose_name=_('Merchant'), related_name='paymentapi', on_delete=models.CASCADE)  
    # Stripe API Credentials
    stripe_public_key = encrypt(models.CharField(_("STRIPE PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    stripe_secret_key = encrypt(models.CharField(_("STRIPE SECRET KEY"), max_length=255, blank=True, null=True))
    stripe_webhook_key = encrypt(models.CharField(_("STRIPE WEEBHOOK KEY(OPTIONAL)"), max_length=255, blank=True, null=True))
    stripe_subscription_price_id = encrypt(models.CharField(_("STRIPE SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    stripe_active = models.BooleanField(_("Status"), choices=((False, 'No'), (True, 'Yes')), default=False)
    stripe_sandbox = models.BooleanField(_("Sandbox Mode"), choices=((False, 'No'), (True, 'Yes')), default=True)
    
    # PayPal API Credentials
    paypal_public_key = encrypt(models.CharField(_("PAYPAL PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    paypal_secret_key = encrypt(models.CharField(_("PAYPAL SECRET KEY"), max_length=255, blank=True, null=True))
    paypal_subscription_price_id = encrypt(models.CharField(_("PAYPAL SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    sandbox = models.BooleanField(_("Sandbox Mode"), choices=((False, 'No'), (True, 'Yes')), default=True)
    paypal_active = models.BooleanField(_("Status"), choices=((False, 'No'), (True, 'Yes')), default=False)
    
    # Paystack API Credentials
    paystack_public_key = encrypt(models.CharField(_("PAYSTACK PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    paystack_secret_key = encrypt(models.CharField(_("PAYSTACK SECRET KEY"), max_length=255, blank=True, null=True))
    paystack_subscription_price_id = encrypt(models.CharField(_("PAYSTACK SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    paystack_active = models.BooleanField(_("Status"), choices=((False, 'No'), (True, 'Yes')), default=False)
    
    
    # Flutterwave API Credentials
    flutterwave_public_key = encrypt(models.CharField(_("FLUTTERWAVE PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    flutterwave_secret_key = encrypt(models.CharField(_("FLUTTERWAVE SECRET KEY"), max_length=255, blank=True, null=True))
    flutterwave_subscription_price_id = encrypt(models.CharField(_("FLUTTERWAVE SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    flutterwave_active = models.BooleanField(_("Status"), choices=((False, 'No'), (True, 'Yes')), default=False)
    
    # Razorpay API Credentials
    razorpay_public_key_id = encrypt(models.CharField(_("RAZORPAY PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    razorpay_secret_key_id = encrypt(models.CharField(_("RAZORPAY SECRET KEY"), max_length=255, blank=True, null=True))
    razorpay_subscription_price_id = encrypt(models.CharField(_("RAZORPAY SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    razorpay_active = models.BooleanField(_("Status"), choices=((False, 'No'), (True, 'Yes')), default=False)
    
    # objects = MerchantAPIsManager()

    def __str__(self):
        return str(self.merchant)

    class Meta:
        verbose_name = 'Merchant API'
        verbose_name_plural = 'Merchant API'


    # def masked_stripe_public_key(self):
    #     if self.stripe_public_key:
    #         return self.stripe_public_key[:4] + '*' * (len(self.stripe_public_key)-5) + self.stripe_public_key[-1]
    #     return None

    def mask_key(self, key):
        '''
        Masks first 4 characters and last 1 character
        '''
        if key:
            return key[:4] + '*' * (len(key)-5) + key[-1]
        return None

    def masked_stripe_public_key(self):
        return self.mask_key(self.stripe_public_key)

    def masked_stripe_secret_key(self):
        return self.mask_key(self.stripe_secret_key)

    def masked_paypal_public_key(self):
        return self.mask_key(self.paypal_public_key)

    def masked_paypal_secret_key(self):
        return self.mask_key(self.paypal_secret_key)


class PaymentAccount(MerchantMaster):
    MOMO = 'mobilemoney'
    BANK = 'bank'
    FLUTTERWAVE_CHOICES = (
        (MOMO, _('Mobile Money')),
        (BANK, _('Bank Account')),
    )  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paymentaccount', on_delete=models.PROTECT,)
    primary_account_type = models.ForeignKey(PaymentGateway, verbose_name=_('Account Type'), related_name='paymntaccountgateway', null=True, blank=True, on_delete=models.SET_NULL,)
    
    paypal_account = encrypt(models.CharField(_("Bearer Account/Email"), max_length=100, help_text=_(
        'Bearer Account Number'), null=True, blank=True))
    paypal_bearer = encrypt(models.CharField(_("Bearer names"), max_length=100, help_text=_(
        'Bearer names'), null=True, blank=True))
    paypal_country = encrypt(models.CharField(_("Bearer Country Name"), max_length=100, help_text=_(
        'Bearer account country. E.g Singapore'), null=True, blank=True))    

    stripe_country = encrypt(models.CharField(_("Bearer Country Name"), max_length=100, help_text=_(
        'Bearer account country. E.g Canada'), null=True, blank=True))    
    stripe_bank = encrypt(models.CharField(_("Bearer Bank Name"), max_length=100, help_text=_(
        'Bearer Bank Name - Account Specific'), null=True, blank=True))    
    stripe_account = encrypt(models.CharField(_("Account Number"), max_length=100, help_text=_(
        'Bearer Account Number'), null=True, blank=True))
    stripe_routing = encrypt(models.CharField(_("Routing Number"), max_length=100, help_text=_(
        'Bearer Routing Number - Country/Bank Specific'), null=True, blank=True))
    stripe_swift_iban = encrypt(models.CharField(_("Swift/Iban code"), max_length=100, help_text=_(
        'Bearer Swift code/Iban- Country/Bank Specific'), null=True, blank=True))
    stripe_bearer = encrypt(models.CharField(_("Bearer Names"), max_length=150, help_text=_(
        'Bearer names'), null=True, blank=True))
    stripe_extra_info = encrypt(models.TextField(_("Extra Credentials"), max_length=100, help_text=_(
        'Additional information to be included'), null=True, blank=True))

    flutterwave_type = encrypt(models.CharField(_("Flutterwave Account Type"), choices=FLUTTERWAVE_CHOICES, default=MOMO, max_length=20))
    flutterwave_bank = encrypt(models.CharField(_("Bearer Bank Names"), max_length=150, help_text=_(
        'Bearer Bank name - Account Type Specific'), null=True, blank=True))
    flutterwave_bearer = encrypt(models.CharField(_("Bearer Names"), max_length=150, help_text=_(
        'Bearer Account names'), null=True, blank=True))
    flutterwave_country = encrypt(models.CharField(_("Bearer Country Name"), max_length=100, help_text=_(
        'Bearer account country. E.g Nigeria'), null=True, blank=True))
    flutterwave_account = encrypt(models.CharField(_("Flutterwave Account Number"), max_length=100, help_text=_(
        'Bearer Account Number'), null=True, blank=True))
    flutterwave_swift_iban = encrypt(models.CharField(_("Swift/Iban"), max_length=100, help_text=_(
        'Swift code/Iban- Country Specific'), null=True, blank=True))
    flutterwave_extra_info = encrypt(models.TextField(_("Extra Credentials"), max_length=100, help_text=_(
        'Additional information to be included'), null=True, blank=True))
    
    razorpay_bearer = encrypt(models.CharField(_("Razorpay Bearer Names"), max_length=150, help_text=_(
        'Bearer Account names'), null=True, blank=True))
    razorpay_upi = encrypt(models.CharField(_("Razorpay UPI ID"), max_length=100, help_text=_(
        'Bearer UPI ID to receive payment'), null=True, blank=True))
    razorpay_country = encrypt(models.CharField(_("Bearer Country Name"), max_length=100, help_text=_(
        'Bearer account country. E.g India'), null=True, blank=True))
    
    created_at = models.DateTimeField(_("Started On"), auto_now_add=True,)  
    modified_on = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'Payment Account'
        verbose_name_plural = 'Payment Account'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


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


class SubscriptionMaster(MerchantMaster):
    BALANCE = 'balance'
    PAYPAL = 'paypal'
    STRIPE = 'stripe'
    PAYSTACK = 'paystack'
    FLUTTERWAVE = 'flutterwave'
    RAZORPAY = 'razorpay'
    PAYMENT_METHODS = (
        (BALANCE, _('Balance')),
        (PAYPAL, _('PayPal')),
        (STRIPE, _('Stripe')),
        (PAYSTACK, _('Paystack')),
        (FLUTTERWAVE, _('Flutterwave')),
        (RAZORPAY, _('Razorpay')),
    )
    payment_method = models.CharField(_("Payment Method"), choices=PAYMENT_METHODS, default=BALANCE, max_length=200)
    price = models.PositiveIntegerField()
    status = models.BooleanField(_("Paid"), choices=((False, 'Failed'), (True, 'Success')), default=False)
    reference = models.CharField(_("Reference"), max_length=200, blank=True, null=True, unique=True)
    customer_token = models.CharField(_("Customer Token"), max_length=2088, blank=True, null=True)
    subscription_id = models.CharField(_("Subscription ID"), max_length=255, blank=True, null=True)    
    created_at = models.DateTimeField(_("Subscription Start"), blank=True, null=True)
    activation_time = models.DateTimeField(_("Activation Time"), blank=True, null=True)
    expired_time = models.DateTimeField(_("Est. Expiration"), blank=True, null=True)
    
    class Meta:
        abstract = True


class Subscription(SubscriptionMaster):
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='subscriptionteam', on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        
    def __str__(self):
        return str(self.team.title)

    def save(self, *args, **kwargs):
        if self.payment_method == 'balance' and not self.reference:
            self.reference = generate_unique_reference(Subscription)
        super().save(*args, **kwargs)


    @classmethod
    def subscribe_with_balance(cls, merchant, team):
        with db_transaction.atomic():
            
            if team is None:
                raise FundException('Error occured. Try in few time')
            
            if merchant is None:
                raise FundException('Error occured. Try in few time')
            
            if team.created_by.fundtransferuser.available_balance < team.team_package.price:
                raise FundException('Insufficuent Balance')
            
            if team.default_plan:
                # THIS CODE WILL ACTIVATE THE PLAN
                subscription = cls.objects.create(
                    team=team,
                    price=team.team_package.price,
                    merchant=merchant,
                    payment_method = cls.BALANCE,
                    created_at=timezone.now(),
                    activation_time=timezone.now(),
                    expired_time = timezone.now() + relativedelta(months = 1)
                )
                subscription.customer_id = team.created_by.pk
                subscription.subscription_id = subscription.reference
                subscription.status = True
                subscription.save()
                FreelancerAccount.charge_freelancer(team.created_by, team.team_package.price)

                user_team = team
                user_team.package = team.team_package
                user_team.package_status = 'active'
                user_team.package_expiry = timezone.now() + relativedelta(months = 1)
                user_team.save()
                # db_transaction.on_commit(lambda: lock_fund_email(account, message))
                return subscription
            else:
                # THIS CODE WILL CANCEL THE PLAN
                user_team = team
                user_team.package = team.basic_package
                user_team.package_status = 'default'
                user_team.package_expiry = None
                user_team.save()

                return user_team

       
    @classmethod
    def subscribe_with_stripe(cls, merchant, team, customer_token, subscription_id, reference):
        
        if team is None:
            raise FundException('Error occured. Try in few time')
        
        if merchant is None:
            raise FundException('Error occured. Try in few time')
    
        subscription = cls.objects.create(
            customer_token=customer_token,
            team=team,
            merchant=merchant,
            payment_method = cls.STRIPE,
            reference = reference,
            subscription_id=subscription_id,
            price=team.team_package.price,
            created_at=timezone.now(),
            activation_time=timezone.now(),
            expired_time = timezone.now() + relativedelta(months = 1)
        )
        subscription.status = False
        subscription.save()
        
        return subscription


    @classmethod
    def stripe_confirmation(cls, subscription_id):
        with db_transaction.atomic():
            subscription = cls.objects.select_for_update().get(subscription_id=subscription_id)
            subscription.status = True
            subscription.save()

            FreelancerAccount.charge_freelancer(subscription.team.created_by, subscription.price)
            
            user_team = subscription.team
            user_team.package = user_team.team_package
            user_team.package_status = 'active'
            user_team.package_expiry = timezone.now() + relativedelta(months = 1)
            user_team.save()
            # db_transaction.on_commit(lambda: lock_fund_email(account, message))
        return subscription


    @classmethod
    def stripe_confirmation(cls, subscription_id):
        with db_transaction.atomic():
            subscription = cls.objects.select_for_update().get(subscription_id=subscription_id)
            subscription.status = True
            subscription.save()

            FreelancerAccount.charge_freelancer(subscription.team.created_by, subscription.price)
            
            user_team = subscription.team
            user_team.package = user_team.team_package
            user_team.package_status = 'active'
            user_team.package_expiry = timezone.now() + relativedelta(months = 1)
            user_team.save()
            # db_transaction.on_commit(lambda: lock_fund_email(account, message))
        return subscription


    @classmethod
    def stripe_cancel(cls, subscription_id):
        pass







