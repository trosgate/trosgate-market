from django.db import models, transaction as db_transaction
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
from general_settings.fund_control import (
    get_min_balance, get_max_receiver_balance, 
    get_min_transfer, get_max_transfer, get_min_withdrawal, 
    get_max_withdrawal, get_min_deposit, 
    get_max_deposit, get_max_depositor_balance,
)
from payments.models import PaymentRequest, AdminCredit
# from general_settings.storage_backend import activate_storage_type, DynamicStorageField
from notification.mailer import initiate_credit_memo_email, credit_pending_balance_email, lock_fund_email
from PIL import Image


class ActiveFreelancer(models.Manager):
    def get_queryset(self):
        return super(ActiveFreelancer, self).get_queryset().filter(user__is_active=True, user__user_type=Customer.FREELANCER)


class Freelancer(models.Model):
    # STORAGE = activate_storage_type()
    MALE = 'male'
    FEMALE = 'female'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )
    # freelancer details
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), related_name="freelancer", on_delete=models.CASCADE)
    merchant = models.ForeignKey('account.Merchant', verbose_name=_('Merchant'), related_name='freelancemerchant', on_delete=models.PROTECT)    
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER)
    tagline = models.CharField(_("Tagline"), max_length=100, blank=True)
    description = models.TextField(_("Description"), max_length=2000, blank=True, error_messages={"name": {"max_length": _("Ensure a maximum character of 2000 for description field")}},)
    brand_name = models.CharField(_("Brand Name"), max_length=60, null=True, blank=True)
    profile_photo = models.ImageField(_("Profile Photo"), upload_to='freelancer/', default='freelancer/user-login.png')
    banner_photo = models.ImageField(_("Banner Photo"),  upload_to='freelancer/', default='freelancer/banner.png')
    department = models.ForeignKey('general_settings.Department', verbose_name=_("Department"),  null=True, blank=True, on_delete=models.RESTRICT)
    business_size = models.ForeignKey('general_settings.Size', verbose_name=_("Business Size"), related_name="freelancers", null=True, blank=True, on_delete=models.RESTRICT)
    address = models.CharField(_("Residence Address"), max_length=100, null=True, blank=True)
    # Skill and Specialty
    skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("General skill"), related_name="freelancerskill")
    keyskill_one = models.CharField(_("Key Skill 1"), max_length=60, null=True, blank=True,)
    key_skill_one_score = models.PositiveIntegerField(_("Key Skill 1 Score"),null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    keyskill_two = models.CharField(_("Key Skill 2"), max_length=60, null=True, blank=True,)
    key_skill_two_score = models.PositiveIntegerField(_("Key Skill 2 Score"),null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    keyskill_three = models.CharField(_("Key Skill 3"), max_length=60, null=True, blank=True,)
    key_skill_three_score = models.PositiveIntegerField(_("Key Skill 3 Score"),null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    keyskill_four = models.CharField(_("Key Skill 4"), max_length=60, null=True, blank=True,)
    key_skill_four_score = models.PositiveIntegerField(_("Key Skill 4 Score"),null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    keyskill_five = models.CharField(_("Key Skill 5"), max_length=60, null=True, blank=True,)
    key_skill_five_score = models.PositiveIntegerField(_("Key Skill 5 Score"),null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])    
    #Experience and Education
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
    # Projects and Awards
    project_title = models.CharField(_("Project Title 1"), max_length=100, null=True, blank=True,)
    project_url = models.URLField(_("Project Url 1"), max_length=2083, null=True, blank=True,)
    image_one = models.ImageField(_("Image 1"), upload_to='freelancer/awards/', null=True, blank=True,)
    project_title_two = models.CharField(_("Project Title 2"), max_length=100, null=True, blank=True,)
    project_url_two = models.URLField(_("Project Url 2"), max_length=2083, null=True, blank=True,)
    image_two = models.ImageField(_("Image 2"), upload_to='freelancer/awards/', null=True, blank=True,)
    project_title_three = models.CharField(_("Project Title 3"), max_length=100, null=True, blank=True,)
    project_url_three = models.URLField(_("Project Url 3"), max_length=2083, null=True, blank=True,)
    image_three = models.ImageField(_("Image 3"), upload_to='freelancer/awards/', null=True, blank=True,)
    slug = models.SlugField(_("Slug"), max_length=30, null=True, blank=True,)
    active_team_id = models.PositiveIntegerField(_("Active Team ID"), default=0)
    objects = models.Manager()
    active = ActiveFreelancer()

    class Meta:
        verbose_name = 'Freelancer Profile'
        verbose_name_plural = 'Freelancer Profile'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        super(Freelancer, self).save(*args, **kwargs)
        new_profile_photo = Image.open(self.profile_photo.path)
        if new_profile_photo.height > 300 or new_profile_photo.width > 300:
            output_size = (300, 300)
            new_profile_photo.thumbnail(output_size)
            new_profile_photo.save(self.profile_photo.path)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                {'start_date': _('End date should be greater tha start date')})

        if self.start_date_two > self.end_date_two:
            raise ValidationError(
                {'end_date': _('End date should be greater tha start date')})

        if self.keyskill_one and self.key_skill_one_score is None:
            raise ValidationError(
                {'key_skill_one_score': _('Skill #1 and Score #1 are required together')})
        
        if self.keyskill_two and self.key_skill_two_score is None:
            raise ValidationError(
                {'key_skill_two_score': _('Skill #2 and Score #2 are required together')})
        
        if self.keyskill_three and self.key_skill_three_score is None:
            raise ValidationError(
                {'key_skill_three_score': _('Skill #3 and Score #3 are required together')})
        
        if self.keyskill_four and self.key_skill_four_score is None:
            raise ValidationError(
                {'key_skill_four_score': _('Skill #4 and Score #4 are required together')})
        
        if self.keyskill_five and self.key_skill_five_score is None:
            raise ValidationError(
                {'key_skill_five_score': _('Skill #5 and Score #5 are required together')})

        return super().clean()


    def freelancer_profile_absolute_url(self):
        return reverse('freelancer:freelancer_profile', args=([(self.user.short_name)]))
    
    def modify_freelancer_absolute_url(self):
        return reverse('freelancer:update_freelancer_profile', args=([(self.user.short_name)]))

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
    merchant = models.ForeignKey('account.Merchant', verbose_name=_('Merchant'), related_name='freelanceaccmerchant', on_delete=models.PROTECT)    
    reference = models.UUIDField(unique=True, verbose_name="Reference Number", editable=False, default=uuid.uuid4,)
    pending_balance = models.PositiveIntegerField(_("Pending Balance"), default=0,)
    available_balance = models.PositiveIntegerField(_("Account Balance"), default=0, help_text=_("Min of $20 and Max of $500 per transaction"),)
    created_at = models.DateTimeField(auto_now=True,)
    modified_on = models.DateTimeField(auto_now=True,)
    lock_fund = models.BooleanField(_("Lock Fund"), default=False,)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Freelancer Account'
        verbose_name_plural = 'Freelancer Account'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

   
    @classmethod
    def lock_freelancer_fund(cls, pk:int, message:str):
        with db_transaction.atomic():
            account = cls.objects.select_for_update().get(pk=pk)
            if account.lock_fund != False:
                raise Exception(_("Error! The account is already locked"))
            account.lock_fund = True
            account.save()

            db_transaction.on_commit(lambda: lock_fund_email(account, message))

        return account


    @classmethod
    def credit_pending_balance(cls, user, pending_balance, purchase):
        with db_transaction.atomic():
            account = cls.objects.select_for_update().get(user=user)
            account.pending_balance += pending_balance
            account.save(update_fields=['pending_balance'])           

            db_transaction.on_commit(lambda: credit_pending_balance_email(account, pending_balance, purchase))
            
        return account
 

    @classmethod
    def initiate_credit_memo(cls, account, user, amount, comment, created_at):
        with db_transaction.atomic():
            account = cls.objects.select_for_update().get(pk=account.id)
            super_admin_user = Customer.objects.select_for_update().get(is_superuser=True)
            owner_active_team = Team.objects.select_for_update().filter(created_by=account.user, status=Team.ACTIVE).first()

            if amount  == '':
                raise FundException(_("Amount is required"))

            if comment == '':
                raise FundException(_('Error! comment is required'))

            if len(comment) > 500:
                raise FundException(_('Error! comment must be less or equal to 500 characters'))
            
            if user.is_assistant == False:
                raise FundException(_("Only Assistant can initiate memo. Be sure to add yourself as assistant under user manager"))

            if not (account.user in owner_active_team.members.all()):
                raise FundException(_("Receiver is no longer a member of his Team. Add first as member"))

            if int(account.available_balance) + int(amount) > int(get_max_depositor_balance()):
                raise FundException(_(f'Adding {amount} will breach the company receiver max({get_max_depositor_balance()}) balance Policy. Please review'))
            
            if not (int(get_min_deposit()) <= int(amount) <= int(get_max_deposit())):
                raise FundException(_(f'Adding {amount} will breach the company Min({get_min_deposit()}) and Max({get_max_deposit()}) deposit policy. Please review'))

            if account.user != owner_active_team.created_by:
                raise FundException(_('Receiver and his Team are not same, so cannot receive credit'))

            credit_memo = AdminCredit.create(
                sender=user,
                receiver=super_admin_user,
                team=owner_active_team,
                comment=comment,
                amount=amount,
                created_at = created_at
            )

            db_transaction.on_commit(lambda: initiate_credit_memo_email(credit_memo))
 
        return account, super_admin_user, owner_active_team, credit_memo


    @classmethod
    def transfer(cls, team_owner, team_staff, team, action_choice, transfer_status, debit_amount, position, gateway=None):
        with db_transaction.atomic():
            team_manager = cls.objects.select_for_update().get(user=team_owner)
            team_member_staff = cls.objects.select_for_update().get(user=team_staff)
            owner_active_team = Team.objects.select_for_update().get(pk=team.id)
            staff_team = Team.objects.select_for_update().filter(created_by=team_staff).first()

            if team_staff is None:
                raise FundException(_("Staff is required"))
                
            if debit_amount  == '':
                raise FundException(_("Amount is required"))

            if position  == '':
                raise FundException(_("Position is required"))

            if team_owner == '':
                raise FundException(_('You must be team Owner to transfer'))

            if team_manager.lock_fund == True:
                raise FundException(_("Sorry! Your account is temporarily locked. Try again later"))

            if not (int(get_min_transfer()) <= int(debit_amount) <= int(get_max_transfer())):
                raise FundException(_(f'Transfer amount is out of range {get_min_transfer()} to {get_max_transfer()}'))

            if int(team_manager.available_balance) - int(debit_amount) < int(get_min_balance()):
                raise FundException(_(f'You cannot keep balance after transaction below {get_min_balance()}'))

            if int(team_member_staff.available_balance) + int(debit_amount) > int(get_max_receiver_balance()):
                raise FundException(_(f'{team_staff} cannot receive funds beyond threshold. Please Prompt receiver to withdraw existing funds first'))

            if int(owner_active_team.team_balance) - int(debit_amount) < int(get_min_balance()):
                raise FundException(_(f'Team balance after transfer cannot fall below {get_min_balance()}'))
            
            if int(debit_amount) > int(owner_active_team.team_balance):
                raise FundException(_(f'Insufficient Team balance: transfer({debit_amount}) bigger than Team Balance({owner_active_team.team_balance})'))
            
            if team_owner != owner_active_team.created_by:
                raise FundException(_('You must be Team founder to initiate transfer'))

            if team_owner == team_staff:
                raise FundException(_('You cannot transfer fund to yourself'))

            team_manager.available_balance -= int(debit_amount)
            team_manager.save(update_fields=['available_balance'])

            owner_active_team.team_balance -= int(debit_amount)
            owner_active_team.save(update_fields=['team_balance'])

            staff_team.team_balance += int(debit_amount)
            staff_team.save(update_fields=['team_balance'])

            team_member_staff.available_balance += int(debit_amount)
            team_member_staff.save(update_fields=['available_balance'])

            account_action = FreelancerAction.create(
                account=team_manager, manager=team_manager.user, team_staff=team_member_staff.user, gateway=gateway, team=owner_active_team, 
                action_choice=action_choice, position=position, debit_amount=debit_amount, transfer_status=transfer_status
            )

        return account_action


    @classmethod
    def withdrawal(cls, team_owner, team, team_staff, gateway, transfer_status, action_choice, withdraw_amount, narration):
        with db_transaction.atomic():
            freelancer_account = cls.objects.select_for_update().get(user=team_owner)
            owner_active_team = Team.objects.select_for_update().get(pk=team.id)

            if narration == '':
                raise FundException(_("narration is required"))

            if len(narration) > 100:
                raise FundException(_("narration exceeds max characters"))

            if withdraw_amount is None:
                raise FundException(_("Withdraw amount is required"))

            if gateway is None:
                raise FundException(_("Payment Account is required"))

            if freelancer_account.lock_fund == True:
                raise FundException(_("Sorry! Your account is temporarily locked. Try again later"))

            if team.created_by != team_owner:
                raise FundException(_('You must be team Owner to transfer'))

            if team_owner != team_staff:
                raise FundException(_('You donnot belong to this Team'))

            if int(withdraw_amount) > int(get_max_withdrawal()):
                raise FundException(_('Ooops! Withdrawal Exceeds Limit'))

            if int(withdraw_amount) < int(get_min_withdrawal()):
                raise FundException(_('You cannot withdraw below Minimum'))

            if int(freelancer_account.available_balance) - int(withdraw_amount) < int(get_min_balance()):
                raise FundException(_(f'You cannot keep balance after withdrawal below {get_min_balance()}'))

            if int(withdraw_amount) == 0:
                raise FundException(_('You cannot set zero Amount'))

            if not (int(get_min_withdrawal()) <= int(withdraw_amount) <= int(get_max_withdrawal())):
                raise FundException(_('Withdraw amount is out of range'))

            if int(owner_active_team.team_balance) - int(withdraw_amount) < int(get_min_balance()):
                raise FundException(_(f'Team balance after witdrawal cannot fall below {get_min_balance()}'))
            
            if int(withdraw_amount) > int(owner_active_team.team_balance):
                raise FundException(_(f'Insufficient Team balance: Withdrawal Amount ({withdraw_amount}) bigger than Team Balance({owner_active_team.team_balance})'))

            if team_owner != owner_active_team.created_by:
                raise FundException(_('You must be Team founder to initiate transfer'))

            freelancer_account.available_balance -= int(withdraw_amount)
            freelancer_account.save(update_fields=['available_balance'])

            owner_active_team.team_balance -= int(withdraw_amount)
            owner_active_team.save(update_fields=['team_balance'])

            account_action = FreelancerAction.create(
                account=freelancer_account,
                manager=freelancer_account.user,
                team=owner_active_team,
                action_choice=action_choice,
                narration=narration,
                gateway=gateway,
                withdraw_amount=withdraw_amount,
                team_staff=freelancer_account.user,
                transfer_status=transfer_status
            )

            payment_request = PaymentRequest.create(
                user=team_owner,
                gateway=str(gateway.name), 
                team=owner_active_team, 
                amount=withdraw_amount
                )
        return account_action, payment_request


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
    merchant = models.ForeignKey('account.Merchant', verbose_name=_('Merchant'), related_name='actionmerchant', on_delete=models.PROTECT)        
    account = models.ForeignKey(FreelancerAccount, verbose_name=_("Account"), related_name="fundmanageraccount", on_delete=models.PROTECT)
    gateway = models.ForeignKey('payments.PaymentGateway', verbose_name=_("Payment Account"), related_name="paymentaccount", blank=True, null=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Manager"), related_name="fundtransferor", on_delete=models.PROTECT)
    team_staff = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Staff"), related_name='fundtransferee', blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='fundtransferteam', on_delete=models.PROTECT)
    position = models.CharField(_("Worked As"), max_length=50,choices=POSITIONS, default=CO_CEO, blank=True, null=True)
    action_choice = models.CharField(_("Action Type"), max_length=50, choices=ACTION_CHOICES, default=NONE, blank=True, null=True)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    transfer_status = models.BooleanField(_("Status"), choices=((False, 'Failed'), (True, 'Successful')), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    narration = models.CharField(_("Withdrawal Narration"), max_length=100, blank=True, null=True)
    debit_amount = models.PositiveIntegerField(_("Transfer Amount"), default=0, blank=True, null=True)
    withdraw_amount = models.PositiveIntegerField(_("Withdraw Amount"), default=0, blank=True, null=True)
    reference = models.CharField(_("Ref Number"), max_length=15, blank=True, help_text=_("This is a unique number assigned for audit purposes"),)
    
    class Meta:
        ordering = ('-id',)
        verbose_name = _("Freelancer Ejournal")
        verbose_name_plural = _("Freelancer Ejournal")

    def __str__(self):
        return f'{self.get_action_choice_display()} by {self.team.title}'

    @classmethod
    def create(cls, account, manager, team, action_choice, transfer_status, gateway=None, debit_amount=None, withdraw_amount=None, team_staff=None, narration=None, position=None):  

        if (action_choice == cls.TRANSFER and team_staff is None):
            raise FundException(_("Staff is required"))

        if (action_choice == cls.TRANSFER and position is None):
            raise FundException(_("position is required"))

        if (action_choice == cls.TRANSFER and gateway is None):
            gateway = None
        
        if (action_choice == cls.TRANSFER and debit_amount is None):
            raise FundException(_("Transfer Amount is required"))

        if (action_choice == cls.WITHDRAWAL and narration is None):
            raise FundException(_("narration is required"))

        if (action_choice == cls.WITHDRAWAL and gateway is None):
            raise FundException(_("Payment Account is required"))

        if (action_choice == cls.WITHDRAWAL and withdraw_amount is None):
            raise FundException(_("Withdraw amount is required"))

        if (action_choice == cls.WITHDRAWAL):
            debit_amount= int(0)

        if (action_choice == cls.WITHDRAWAL):
            team_staff = None

        if (action_choice == cls.WITHDRAWAL):
            position = ''

        if (action_choice == cls.TRANSFER):
            withdraw_amount= int(0)

        if (action_choice == cls.TRANSFER):
            narration= ''

        action = cls.objects.create(
            account=account, 
            manager=manager, 
            team=team, 
            gateway=gateway, 
            action_choice=action_choice, 
            transfer_status=transfer_status,
            debit_amount=debit_amount, 
            withdraw_amount=withdraw_amount, 
            team_staff=team_staff, 
            position=position, 
            narration=narration
        )
        stan = f'{action.pk}'.zfill(8)
        action.reference = f'EJ-{stan}'
        action.save()       
        
        return action
