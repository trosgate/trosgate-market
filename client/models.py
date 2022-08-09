from django.db import models, transaction
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from account.fund_exception import FundException
from general_settings.fund_control import get_max_deposit, get_min_deposit, get_max_depositor_balance, get_min_depositor_balance
from general_settings.storage_backend import activate_storage_type, DynamicStorageField


class Client(models.Model):
    STORAGE = activate_storage_type()
    MALE = 'male'
    FEMALE = 'female'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )
    # Client and freelancer details
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_(
        "Client"), related_name="clients", on_delete=models.CASCADE)
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER)
    budget_per_hourly_rate = models.IntegerField(
        _("Budget/Hourly"), default=5, validators=[MinValueValidator(5), MaxValueValidator(500)])
    tagline = models.CharField(_("Tagline"), max_length=100, blank=True)
    description = models.TextField(_("Description"), max_length=2000, blank=True, error_messages={
                                   "name": {"max_length": _("A maximum of 2000 words required")}},)
    brand_name = models.CharField(
        _("Brand Name"), max_length=60, null=True, blank=True)
    profile_photo = models.ImageField(
        _("Profile Photo"), upload_to='client/', default='client/avatar5.png')
    company_logo = models.ImageField(
        _("Brand Logo"),  upload_to='client/', default='client/logo.png')
    banner_photo = models.ImageField(
        _("Banner Photo"),  upload_to='client/', default='client/banner.png')
    business_size = models.ForeignKey("general_settings.Size", verbose_name=_(
        "Business Size"), related_name="clients", null=True, blank=True, on_delete=models.PROTECT)
    address = models.CharField(
        _("Residence Address"), max_length=100, null=True, blank=True)
    skill = models.ManyToManyField(
        "general_settings.Skill", verbose_name=_("skill"), related_name="clientskill")
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="employeefreelancer", default=None, blank=True)
    announcement = models.TextField(
        _("Announcement"), max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profile'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # a url route for the profile detail page
    def client_profile_get_absolute_url(self):
        return reverse('client:client_profile', args=([(self.user.short_name)]))

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='clientfunduser', on_delete=models.PROTECT,)
    debug_balance = models.PositiveIntegerField(_("Pending Balance"), default=0)
    available_balance = models.PositiveIntegerField(_("Account Balance"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client Account'
        verbose_name_plural = 'Client Account'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


    @classmethod
    def level_one_deposit_check(cls, user, deposit_amount, narration, reference, deposit_fee):
        with transaction.atomic():
            client_account = cls.objects.select_for_update().get(user=user)

            if not deposit_amount:
                raise FundException(_("Deposit amount is required"))

            if not (int(get_min_deposit()) <= int(deposit_amount) <= int(get_max_deposit())):
                raise FundException(_('Deposit amount is out of range'))

            if int(client_account.available_balance) + int(deposit_amount) > int(get_max_depositor_balance()):
                raise FundException(_('Maximum account balance exceeded'))

            if int(client_account.available_balance) + int(deposit_amount) < int(get_min_depositor_balance()):
                raise FundException(_('Deposited amount is below minimum'))

            client_account.available_balance += int(0)
            client_account.save(update_fields=['available_balance'])

            account_action = ClientAction.create(
                account=client_account, narration=narration, deposit_amount=deposit_amount, deposit_fee=deposit_fee, reference=reference, status=False
            )

        return client_account, account_action


    @classmethod
    def level_two_deposit_check(cls, transaction_id, depositor, deposit_amount, deposit_fee, reference):
        with transaction.atomic():
            client_account = cls.objects.select_for_update().get(user=depositor)

            if not deposit_amount:
                raise FundException(_("Deposit amount is required"))

            client_account.available_balance += int(deposit_amount)
            client_account.save(update_fields=['available_balance'])

            account_action = cls.objects.select_for_update().get(account=client_account, transaction_id=transaction_id, reference=reference, status=False)

            account_action.available_balance += int(deposit_amount)
            account_action.status = True
            account_action.save(update_fields=['available_balance', 'status'])

        return client_account, account_action


class ClientAction(models.Model):
    account = models.ForeignKey(ClientAccount, verbose_name=_("Account"), related_name="clientfundaccount", on_delete=models.PROTECT)
    narration = models.CharField(_("Deposit Narration"), max_length=100, blank=True, null=True)
    stripe_order_id = models.CharField(_("Stripe Order ID"), max_length=100, blank=True, null=True)
    deposit_amount = models.PositiveIntegerField(_("Deposit Amount"), default=0)
    deposit_fee = models.PositiveIntegerField(_("Deposit Fee"), default=0)
    reference = models.CharField(_("Reference"), max_length=100)
    status = models.BooleanField(_("Status"), choices=((False, 'Failed'), (True, 'Success')), default=False)

    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Client Action")
        verbose_name_plural = _("Client Action")

    def __str__(self):
        return self.account.user.get_full_name()

    @classmethod
    def create(cls, account, deposit_amount, deposit_fee, reference, narration, status=None):

        if not account:
            raise FundException(_("You donnot qualify for this operation"))

        if not deposit_amount:
            raise FundException(_("Amount must be specified"))

        if not deposit_fee:
            raise FundException(_("fee type not specified"))

        if not reference:
            raise FundException(_("Reference must be specified"))

        if not narration:
            raise FundException(_("Narration not specified"))

        action = cls.objects.create(
            account=account, deposit_amount=deposit_amount, deposit_fee=deposit_fee, narration=narration, reference=reference)
        return action
