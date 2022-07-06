from django.db import models, transaction
from django.db.models import F, Q
import uuid
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.utilities import create_random_code
from account.models import Customer
from account.fund_exception import FundException
from teams.models import Team
from general_settings.fund_control import get_min_balance, get_max_receiver_balance, get_min_transfer, get_max_transfer, get_min_withdrawal, get_max_withdrawal


class ActiveFreelancer(models.Manager):
    def get_queryset(self):
        return super(ActiveFreelancer, self).get_queryset().filter(user__is_active=True, user__user_type=Customer.FREELANCER)


class Freelancer(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )
    # freelancer details
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), related_name="freelancer", on_delete=models.CASCADE)
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER)
    hourly_rate = models.IntegerField(_("Hourly Rate"), default=5, validators=[MinValueValidator(5), MaxValueValidator(500)])
    tagline = models.CharField(_("Tagline"), max_length=100, blank=True)
    description = models.TextField(_("Description"), max_length=2000, blank=True, error_messages={"name": {"max_length": _("Ensure a maximum character of 2000 for description field")}},)
    brand_name = models.CharField(_("Brand Name"), max_length=60, null=True, blank=True)
    support = models.CharField(unique=True, max_length=15, null=True, blank=True,)
    profile_photo = models.ImageField(_("Profile Photo"), upload_to='freelancer/', default='freelancer/avatar5.png')
    banner_photo = models.ImageField(_("Banner Photo"),  upload_to='freelancer/', default='freelancer/banner.png')
    department = models.ForeignKey('general_settings.Department', verbose_name=_("Department"),  null=True, blank=True, on_delete=models.RESTRICT)
    business_size = models.ForeignKey('general_settings.Size', verbose_name=_("Business Size"), related_name="freelancers", null=True, blank=True, on_delete=models.RESTRICT)
    address = models.CharField(_("Residence Address"), max_length=100, null=True, blank=True)
    skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("skill"), related_name="freelancerskill")
    #Experience and Education(freelancer)
    company_name = models.CharField(_("Company Name 1"), max_length=100, null=True, blank=True,)
    start_date = models.DateField(_("Start Date 1"), default=timezone.now,auto_now_add=False, auto_now=False, null=True, blank=True,)
    end_date = models.DateField(_("End Date 1"), default=timezone.now,auto_now_add=False, auto_now=False, null=True, blank=True,)
    job_position = models.CharField(_("Job Position 1"), max_length=100, null=True, blank=True,)
    job_description = models.TextField(_("Job Description 1"), max_length=500, null=True, blank=True,)
    company_name_two = models.CharField(_("Company Name 2"), max_length=100, null=True, blank=True,)
    start_date_two = models.DateField(_("Start Date 2"), default=timezone.now, auto_now_add=False, auto_now=False, null=True, blank=True,)
    end_date_two = models.DateField(_("End Date 2"), default=timezone.now, auto_now_add=False, auto_now=False, null=True, blank=True,)
    job_position_two = models.CharField(_("Job Position 2"), max_length=100, null=True, blank=True,)
    job_description_two = models.TextField(_("Job Description 2"), max_length=500, null=True, blank=True,)
    #Projects and Awards(freelancer)
    project_title = models.CharField(_("Project Title 1"), max_length=100, null=True, blank=True,)
    project_url = models.URLField(_("Project Url 1"), max_length=2083, null=True, blank=True,)
    image_one = models.ImageField(_("Image 1"), upload_to='freelancer/awards/',default='freelancer/awards/banner.png', null=True, blank=True,)
    project_title_two = models.CharField(_("Project Title 2"), max_length=100, null=True, blank=True,)
    project_url_two = models.URLField(_("Project Url 2"), max_length=2083, null=True, blank=True,)
    image_two = models.ImageField(_("Image 2"), upload_to='freelancer/awards/',default='freelancer/awards/banner.png', null=True, blank=True,)
    project_title_three = models.CharField(_("Project Title 3"), max_length=100, null=True, blank=True,)
    project_url_three = models.URLField(_("Project Url 3"), max_length=2083, null=True, blank=True,)
    image_three = models.ImageField(_("Image 3"), upload_to='freelancer/awards/',default='freelancer/awards/banner.png', null=True, blank=True,)
    slug = models.SlugField(_("Slug"), max_length=30, null=True, blank=True,)
    active_team_id = models.PositiveIntegerField(_("Active Team ID"), default=0)
    active = ActiveFreelancer()

    class Meta:
        verbose_name = 'Freelancer Profile'
        verbose_name_plural = 'Freelancer Profile'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if self.support is None:
            self.support = 'Fr-' + create_random_code()[:10]
        super(Freelancer, self).save(*args, **kwargs)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                {'start_date': _('End date should be greater tha start date')})

        if self.start_date_two > self.end_date_two:
            raise ValidationError(
                {'end_date': _('End date should be greater tha start date')})

        return super().clean()

    # a url route for the profile detail page

    def freelancer_profile_absolute_url(self):
        return reverse('freelancer:freelancer_profile', args=([(self.user.short_name)]))

    # image display in Admin
    def image_tag(self):
        if self.profile_photo:
            return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.profile_photo))
        else:
            return f'/static/images/user-login.png'

    image_tag.short_description = 'profile_photo'

    # image display in Admin
    def banner_tag(self):
        return mark_safe('<img src="/media/%s" width="100" height="50" />' % (self.banner_photo))

    banner_tag.short_description = 'banner_photo'


class FreelancerAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='fundtransferuser', on_delete=models.PROTECT,)
    reference = models.UUIDField(unique=True, verbose_name="Reference Number", editable=False, default=uuid.uuid4,)
    # pending_balance = models.PositiveIntegerField(_("Pending Balance"), default=0,)
    available_balance = models.PositiveIntegerField(_("Account Balance"), default=0, help_text=_("Min of $20 and Max of $500 per transaction"),)
    created_at = models.DateTimeField(auto_now=True,)
    modified_on = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'Freelancer Account'
        verbose_name_plural = 'Freelancer Account'

    def __str__(self):
        return self.user.short_name
 

    @classmethod
    def transfer(cls, team_owner, team_staff, team, action_choice, transfer_status, debit_amount, position):

        with transaction.atomic():
            team_manager = cls.objects.select_for_update().get(user=team_owner)
            team_member_staff = cls.objects.select_for_update().get(user=team_staff)

            if not team_staff:
                raise FundException(_("Staff is required"))
                
            if not debit_amount:
                raise FundException(_("Amount is required"))

            if not position:
                raise FundException(_("Position is required"))

            if not team_owner:
                raise FundException(_('You must be team Owner to transfer'))

            if int(debit_amount) > int(get_max_transfer()):
                raise FundException(_('Transfer Exceeds Limit'))

            if int(debit_amount) < int(get_min_transfer()):
                raise FundException(_('You cannot Transfer below Minimum'))

            if not (int(get_min_transfer()) <= int(debit_amount) <= int(get_max_transfer())):
                raise FundException(_('Transfer amount is out of range'))

            if int(team_manager.available_balance) - int(debit_amount) < int(get_min_balance()):
                raise FundException(_('You cannot keep balance after transaction below minimum'))

            if int(team_member_staff.available_balance) + int(debit_amount) > int(get_max_receiver_balance()):
                raise FundException(_('Unsuccessful. Please Prompt Receiver to withdraw existing funds first'))

            if team_owner == team_staff:
                raise FundException(_('You cannot transfer fund to yourself'))

            team_manager.available_balance -= int(debit_amount)
            team_manager.save(update_fields=['available_balance'])

            team_member_staff.available_balance += int(debit_amount)
            team_member_staff.save(update_fields=['available_balance'])

            account_action = FreelancerAction.objects.create(
                account=team_manager, manager=team_manager.user, team_staff=team_member_staff.user, team=team, 
                action_choice=action_choice, position=position, debit_amount=debit_amount, transfer_status=transfer_status
            )

        return account_action

    @classmethod
    def withdrawal(cls, team_owner, team, team_staff, transfer_status, action_choice, withdraw_amount, narration):
        with transaction.atomic():
            freelancer_account = cls.objects.select_for_update().get(user=team_owner)

            if not narration:
                raise FundException(_("narration is required"))

            if not withdraw_amount:
                raise FundException(_("Withdraw amount is required"))

            if team.created_by != team_owner:
                raise FundException(_('You must be team Owner to transfer'))

            if team_owner != team_staff:
                raise FundException(_('You donnot belong to this Team'))

            if int(withdraw_amount) > int(get_max_withdrawal()):
                raise FundException(_('Ooops! Withdrawal Exceeds Limit'))

            if int(withdraw_amount) < int(get_min_withdrawal()):
                raise FundException(_('You cannot withdraw below Minimum'))

            if int(freelancer_account.available_balance) - int(withdraw_amount) < int(get_min_balance()):
                raise FundException(_('You cannot keep balance below Minimum'))

            if int(withdraw_amount) == 0:
                raise FundException(_('You cannot set zero Amount'))

            if not (int(get_min_withdrawal()) <= int(withdraw_amount) <= int(get_max_withdrawal())):
                raise FundException(_('Withdraw amount is out of range'))

            freelancer_account.available_balance -= int(withdraw_amount)
            freelancer_account.save(update_fields=['available_balance'])

            account_action = FreelancerAction.create(
                account=freelancer_account,
                manager=freelancer_account.user,
                team=team,
                action_choice=action_choice,
                narration=narration,
                withdraw_amount=withdraw_amount,
                team_staff=freelancer_account.user,
                transfer_status=transfer_status
            )

        return account_action


class FreelancerAction(models.Model):
    # Positions
    CEO = 'ceo'
    CO_CEO = 'co_ceo'
    GENERAL_MANAGER = 'general_manager'
    MARKETING_MANAGER = 'marketing_manager'
    VIRTUAL_ASSISTANT = 'virtual_assistant'
    SALES_REP = 'sales_rep'
    ANALYST = 'analyst'
    PRO = 'pro'
    POSITIONS = (
        (CEO, _("CEO")),
        (CO_CEO, _("CO-CEO")),
        (GENERAL_MANAGER, _("General Manager")),
        (MARKETING_MANAGER, _("Marketing Manager")),
        (VIRTUAL_ASSISTANT, _("Virtual Assistant")),
        (SALES_REP, _("Sales Rep")),
        (ANALYST, _("Analyst")),
        (PRO, _("PRO")),
    )
    # Action Choices
    NONE = 'none'
    TRANSFER = 'transfer'
    WITHDRAWAL = 'withdrawal'
    ACTION_CHOICES = (
        (NONE, _("None")),
        (TRANSFER, _("Transfer")),
        (WITHDRAWAL, _("Withdrawal")),
    )

    account = models.ForeignKey(FreelancerAccount, verbose_name=_("Account"), related_name="fundmanageraccount", on_delete=models.PROTECT)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Manager"), related_name="fundtransferor", on_delete=models.PROTECT)
    team_staff = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Staff"), related_name='fundtransferee', blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='fundtransferteam', on_delete=models.PROTECT)
    position = models.CharField(_("Worked As"), max_length=50,choices=POSITIONS, default=CO_CEO, blank=True, null=True)
    action_choice = models.CharField(_("Worked As"), max_length=50, choices=ACTION_CHOICES, default=NONE, blank=True, null=True)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    transfer_status = models.BooleanField(_("Status"), choices=((False, 'Failed'), (True, 'Successful')), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    narration = models.CharField(_("Withdrawal Narration"), max_length=100, blank=True, null=True)
    debit_amount = models.PositiveIntegerField(_("Transfer Amount"), default=0, blank=True, null=True)
    withdraw_amount = models.PositiveIntegerField(_("Withdraw Amount"), default=0, blank=True, null=True)
    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Freelancer Action")
        verbose_name_plural = _("Freelancer Action")

    def __str__(self):
        return f'{self.team.title} - {self.position}'

    @classmethod
    def create(cls, account, manager, team, action_choice, transfer_status, debit_amount=None, withdraw_amount=None, team_staff=None, narration=None, position=None):  # 'delta_amount',

        if (action_choice == cls.TRANSFER and team_staff is None):
            raise FundException(_("Staff is required"))

        if (action_choice == cls.TRANSFER and position is None):
            raise FundException(_("position is required"))

        if (action_choice == cls.TRANSFER and debit_amount is None):
            raise FundException(_("Transfer Amount is required"))

        if (action_choice == cls.WITHDRAWAL and narration is None):
            raise FundException(_("narration is required"))

        if (action_choice == cls.WITHDRAWAL and withdraw_amount is None):
            raise FundException(_("Withdraw amount is required"))

        action = cls.objects.create(account=account, manager=manager, team=team, action_choice=action_choice, transfer_status=transfer_status,
                                    debit_amount=debit_amount, withdraw_amount=withdraw_amount, team_staff=team_staff, position=position, narration=narration)
        return action
