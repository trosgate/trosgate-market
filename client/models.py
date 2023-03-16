from django.db import models, transaction as db_transaction
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from account.fund_exception import FundException
from general_settings.fund_control import get_max_deposit, get_min_deposit, get_max_depositor_balance, get_min_depositor_balance
from general_settings.currency import get_base_currency_symbol, get_base_currency_code



class Client(models.Model):
    # STORAGE = activate_storage_type()
    MALE = 'male'
    FEMALE = 'female'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )
    # Client and freelancer details
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("Client"), 
        related_name="clients", 
        on_delete=models.CASCADE
    )
    merchant = models.ForeignKey(
        'account.Merchant', 
        verbose_name=_('Merchant'), 
        related_name='clientmerchant', 
        on_delete=models.PROTECT
    )
    gender = models.CharField(
        _("Gender"), 
        max_length=10, 
        choices=GENDER
    )

    tagline = models.CharField(
        _("Tagline"), 
        max_length=100, 
        blank=True
    )
    description = models.TextField(
        _("Description"), 
        max_length=2000, 
        blank=True, 
        error_messages={"name": {"max_length": _("A maximum of 2000 words required")}},
    )
    brand_name = models.CharField(
        _("Brand Name"), 
        max_length=60, 
        null=True, 
        blank=True
    )
    profile_photo = models.ImageField(
        _("Profile Photo"), 
        upload_to='client/', 
        default='client/avatar5.png'
    )
    company_logo = models.ImageField(
        _("Brand Logo"), 
        upload_to='client/', 
        default='client/logo.png'
    )
    banner_photo = models.ImageField(
        _("Banner Photo"), 
        upload_to='client/', 
        default='client/banner.png'
    )
    business_size = models.ForeignKey(
        "general_settings.Size", 
        verbose_name=_("Business Size"), 
        related_name="clients", 
        null=True, 
        blank=True, 
        on_delete=models.PROTECT
    )
    department = models.ForeignKey(
        'general_settings.Department', 
        verbose_name=_("Department"),  
        null=True, 
        blank=True, 
        on_delete=models.PROTECT
    )    
    address = models.CharField(
        _("Residence Address"), 
        max_length=100, 
        null=True, 
        blank=True
    )
    skill = models.ManyToManyField(
        "general_settings.Skill", 
        verbose_name=_("skill"), 
        related_name="clientskill"
    )
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="employeefreelancer", 
        default=None, 
        blank=True
    )
    announcement = models.TextField(
        _("Announcement"), 
        max_length=1000, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profile'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # a url route for the profile detail page
    def client_profile_get_absolute_url(self):
        return reverse('client:client_profile', args=([(self.user.short_name)]))
    
    def modify_client_get_absolute_url(self):
        return reverse('client:update_client_profile', args=([(self.user.short_name)]))

    # profile image display in Admin
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.profile_photo))
    
    image_tag.short_description = 'profile_photo'

    # banner image display in Admin
    def banner_tag(self):
        return mark_safe('<img src="/media/%s" width="100" height="50" />' % (self.banner_photo))

    banner_tag.short_description = 'banner_photo'

    # logo image display in Admin
    def logo_tag(self):
        return mark_safe('<img src="/media/%s" width="100" height="50" />' % (self.company_logo))

    logo_tag.short_description = 'company_logo'


class ClientAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='clientfunduser', 
        on_delete=models.PROTECT,
    )
    merchant = models.ForeignKey(
        'account.Merchant', 
        verbose_name=_('Merchant'), 
        related_name='clientactmerchant', 
        on_delete=models.PROTECT
    )    
    debug_balance = models.PositiveIntegerField(_("Pending Balance"), default=0)
    available_balance = models.PositiveIntegerField(_("Account Balance"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user__pk',)
        verbose_name = 'Client Account'
        verbose_name_plural = 'Client Account'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


    @classmethod
    def debit_available_balance(cls, user, available_balance):
        with db_transaction.atomic():
            account = cls.objects.select_for_update().get(user=user)
            account.available_balance -= available_balance
            account.save(update_fields=['available_balance'])           
            db_transaction.on_commit(lambda: print('client debited:', account, available_balance))
        return account


    @classmethod
    def deposit_check(cls, user, deposit_amount, narration):
        with db_transaction.atomic():
            client_account = cls.objects.select_for_update().get(user=user)

            if client_account.user.first_name == '':
                raise FundException(_("Please complete your profile to perform this task"))

            if client_account.user.last_name == '':
                raise FundException(_("Please complete your profile to perform this task"))

            if narration == '':
                raise FundException(_("Narration is required"))

            if deposit_amount == '':
                raise FundException(_("Deposit amount is required"))

            if deposit_amount > get_max_deposit():
                raise FundException(_(f"Invalid amount entered. Amount > {get_max_deposit()}"))

            if not (int(get_min_deposit()) <= int(deposit_amount) <= int(get_max_deposit())):
                raise FundException(_(f'Deposit amount is out of value range {get_min_deposit()} - {get_max_deposit()}'))

            if int(client_account.available_balance) + int(deposit_amount) > int(get_max_depositor_balance()):
                raise FundException(_('Maximum account balance exceeded'))

            if int(client_account.available_balance) + int(deposit_amount) < int(get_min_depositor_balance()):
                raise FundException(_('Deposited amount is below minimum'))

        return client_account


    @classmethod
    def final_deposit(cls, user, amount, deposit_fee, narration, gateway):
        with db_transaction.atomic():
            client_account = cls.objects.select_for_update().get(user=user)

            if user is None:
                raise FundException(_("Sorry! deposit operation failed"))

            if amount == '':
                raise FundException(_("Amount must be specified"))
            
            if deposit_fee == '':
                raise FundException(_("We could not verify the selected payment method. Try again"))

            if narration == '':
                raise FundException(_("Narration must be specified"))
            
            if gateway == '':
                raise FundException(_("something went wrong on our side. Check back in few minutes. "))

            client_account.available_balance += int(amount)
            client_account.save(update_fields=['available_balance'])

            account_action = ClientAction.create(
                account=client_account, 
                narration=narration, 
                amount=amount, 
                deposit_fee=deposit_fee, 
                gateway=gateway
            )

        return client_account, account_action


class ClientAction(models.Model):
    account = models.ForeignKey(
        ClientAccount, 
        verbose_name=_("Account"), 
        related_name="clientfundaccount", 
        on_delete=models.PROTECT
    )
    merchant = models.ForeignKey(
        'account.Merchant', 
        verbose_name=_('Merchant'), 
        related_name='merchantaction', 
        on_delete=models.PROTECT
    )    
    narration = models.CharField(_("Narration"), max_length=100, blank=True, null=True)
    amount = models.PositiveIntegerField(_("Amount"), default=0,)
    deposit_fee = models.PositiveIntegerField(_("Deposit Fee"), default=0,)
    status = models.BooleanField(_("Status"), choices=((False, 'Failed'), (True, 'Paid')), default=False)
    gateway = models.CharField(_("Payment Method"), max_length=20)
    created_at = models.DateTimeField(_("Deposited On"), auto_now_add=True,)
    reference = models.CharField(_("Ref Number"), max_length=15, blank=True, help_text=_("This is a unique number assigned for audit purposes"),)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Deposit Ejournal'
        verbose_name_plural = 'Deposit Ejournal'

    def __str__(self):
        return f'{self.account.user.first_name} {self.account.user.last_name}'

    @classmethod
    def create(cls, account, amount, deposit_fee, narration, gateway):
        deposit =  cls.objects.create(account=account, amount=amount, deposit_fee=deposit_fee, narration=narration, gateway=gateway, status=True)
        stan = f'{deposit.pk}'.zfill(8)
        deposit.reference = f'DEP-{stan}'
        deposit.save()
        return deposit  
