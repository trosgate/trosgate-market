from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models, transaction as db_transaction
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from . utilities import create_random_code
from account.fund_exception import InvitationException
import secrets
from account.models import Customer
from general_settings.fund_control import get_min_balance, get_max_receiver_balance, get_min_transfer, get_max_transfer, get_min_withdrawal, get_max_withdrawal
from django.utils.text import slugify
from merchants.models import MerchantMaster
from django.core.exceptions import ValidationError
from django.db.models  import F, Sum
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def code_generator():
    generated_code = secrets.token_urlsafe(6)[:6]
    similar_ref = Invitation.objects.filter(code=generated_code)
    while not similar_ref:
        code = generated_code
        break
    return code


class Package(MerchantMaster):
    #
    # Team statuses
    BASIC = 'basic'
    TEAM = 'team'
    STATUS =(
        (BASIC, _('Basic')),
        (TEAM, _('Subscription'))
    )

    #
    #Initial Plan Configuration
    type = models.CharField(_("Package Type"), choices=STATUS, max_length=20)  
    max_proposals_allowable_per_team = models.PositiveIntegerField(_("Max Proposals Per Team"), default=5, help_text=_("You can add min of 5 and max of 50 Proposals per Team"), validators=[MinValueValidator(5), MaxValueValidator(50)])
    monthly_projects_applicable_per_team = models.PositiveIntegerField(_("Monthly Applications Per Team"), default=5, help_text=_("Monthly Jobs Applications with min of 5 and max 50"), validators=[MinValueValidator(5), MaxValueValidator(50)])
    monthly_offer_contracts_per_team = models.PositiveIntegerField(_("Monthly Offer Contracts"), default=5, help_text=_("Clients can view team member's profile and send offer Contracts up to 100 monthly"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_member_per_team = models.PositiveIntegerField(_("Max Member per Team"), default=1, help_text=_("A freelancer can invite upt this number inclusive"), validators=[MinValueValidator(0), MaxValueValidator(4)])
    price = models.PositiveIntegerField(_("Price"), default=0)
    ordering = models.PositiveIntegerField(_("Display"), default=1, help_text=_("This determines how each package will appear to user eg, 1 means first position"), validators=[MinValueValidator(1), MaxValueValidator(3)])
 
    class Meta:
        ordering = ('ordering',)
        verbose_name = _("Upsell Package")
        verbose_name_plural = _("Upsell Packages")
        unique_together = ['type', 'merchant']

    def __str__(self):
        return str(self.get_type_display())

    def save(self, *args, **kwargs):
        if self.type == Package.TEAM:
            self.price = (self.merchant.packages.price * 0.6)
        else:
            self.price = 0
        super(Package, self).save(*args, **kwargs)


class Team(MerchantMaster):
    #
    # Team status
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS = (
        (ACTIVE, _('Active')),
        (INACTIVE, _('Inactive'))
    )

    # Package status
    DEFAULT = 'default'
    ACTIVE = 'active'
    PACKAGE_STATUS = (
        (DEFAULT, 'Default Plan'),
        (ACTIVE, 'Active Plan')
    )

    title = models.CharField(_("Title"), max_length=100, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Team Founder"), related_name="teammanager", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, verbose_name=_("Team Plan"), related_name="teams", on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Team Members"), related_name='team_member', through="TeamMember")
    notice = models.TextField(_("Purpose/Mission"), max_length=2000)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    status = models.CharField(_("Team Status"), max_length=20, choices=STATUS, default=ACTIVE)
    package_status = models.CharField(_("Package Status"), max_length=20, choices=PACKAGE_STATUS, default=DEFAULT)
    package_expiry = models.DateTimeField(_("Package Expiry Date"), blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=100, editable=True)
    team_balance = models.PositiveIntegerField(_("Team Balance"), default=0, help_text=_("Team Transaction Balance"),)
    # payment method to be used by User to activate plan
    stripe_customer_id = models.CharField(_("Stripe Customer ID"), max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(_("Stripe Subscription ID"), max_length=255, blank=True, null=True)
    paypal_customer_id = models.CharField(_("Paypal Customer ID"), max_length=255, blank=True, null=True)
    paypal_subscription_id = models.CharField(_("Paypal Subscription ID"), max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(_("Razorpay Payment ID"), max_length=255, blank=True, null=True)
    razorpay_subscription_id = models.CharField(_("Razorpay Subscription ID"), max_length=255, blank=True, null=True)
    razorpay_payment_url = models.CharField(_("Razorpay Short_Link"), max_length=255, blank=True, null=True)

    # team projects to display
    gallery_link = models.URLField(_("Sample Website"), max_length=2083, help_text=_("A link to your gallery of greaat jobs done"), null=True, blank=True)

    def __str__(self):
        return self.title

    def tracking_time(self):
        return sum(tracker.minutes for tracker in self.trackings.all())

    def get_team_detail_absolute_url(self):
        return reverse('teams:team_single', args=[self.id])

    def get_team_update_absolute_url(self):
        return reverse('teams:update_team', args=[self.id])

    def get_team_delete_absolute_url(self):
        return reverse('teams:delete_team', args=[self.id])

    def get_team_activated_url(self):
        return reverse('teams:activate_team', args=[self.id])

    def get_team_preview_url(self):
        return reverse('teams:preview_inactive_team', args=[self.id])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    @classmethod
    def create_team_with_member(cls, title, created_by, package, merchant, notice='Default team'):
        with db_transaction.atomic():
            team = cls.objects.create(
                title=title, 
                created_by=created_by, 
                package=package,
                notice=notice, 
                merchant=merchant
            )
            team.slug = slugify(created_by.short_name)
            team.save()

            TeamMember.create(
                team=team,
                member=team.created_by,
                earning_ratio=100
            )

            Invitation.founder_invitation(
                team=team, 
                type=Invitation.INTERNAL, 
                status=Invitation.ACCEPTED
            )
            
        return team


    @property
    def max_member_per_team(self):
        # Checks that the team qualifies to invite new members
        max_member_invite = self.package.max_member_per_team > self.invitations.count()
        return self.package.type == Package.TEAM and self.package_status == Team.ACTIVE and max_member_invite

    @property
    def show_max_member_message(self):
        # Messages to show when team.max_member_per_team() is false
        max_member_invite = self.package.max_member_per_team > self.invitations.count()
        if self.package.type == Package.BASIC or self.package_status == Team.DEFAULT:
            message = "Upgrade team to invite"
        if self.package.type == Package.TEAM and self.package_status == Team.ACTIVE and not max_member_invite:
            message = "Maximum invite reached for this team"
        if self.package.type == Package.TEAM and self.package_status != Team.ACTIVE:
            message = "Renew subscription for this team"
        return message

    @property
    def max_proposals_allowable_per_team(self):
        return self.package.max_proposals_allowable_per_team > self.proposalteam.count()

    @property
    def show_max_proposal_message(self):
        # Messages to show when team.max_proposals_allowable_per_team() is false   
        checker = self.max_proposals_allowable_per_team
        return "Limit reached for active team's package" if not checker else ''

    @property
    def monthly_contract_slot(self):
        team_contracts_limit = self.package.monthly_offer_contracts_per_team
        monthly_team_contracts_count = self.contracts.filter(
            date_created__gt=timezone.now() - relativedelta(months=1)
        ).prefetch_related('team').count()
        print('monthly_team_contracts_count :gdgdgdg:', monthly_team_contracts_count)     
        return team_contracts_limit > monthly_team_contracts_count

    @property
    def show_monthly_contract_message(self):
        # Messages to show when team.monthly_contract_slot() is false   
        checker = self.monthly_contract_slot
        return "does not have open slot for contracts" if not checker else ''

    @property
    def monthly_projects_slot(self):
        team_project_limit = self.team.package.monthly_projects_applicable_per_team

        applications = self.application_set.filter(
            created_at__gt=timezone.now() - relativedelta(months=1)
        ).prefetch_related('team')

        monthly_applications_count = len(applications)

        return team_project_limit > monthly_applications_count


    @classmethod
    @db_transaction.atomic
    def split_earnings(cls):
        team = cls.team  # Store the team instance to avoid repeated attribute access
        
        active_relationships = team.teammember_set.filter(is_active=True).select_related('member')
        
        if active_relationships.count() == 0:
            raise ValueError("No active team members to split earnings.")
        
        total_ratio = sum(relationship.earning_ratio for relationship in active_relationships)
        earnings = {}

        non_zero_relationships = [relationship for relationship in active_relationships if relationship.earning_ratio > 0]
        non_zero_total_ratio = sum(relationship.earning_ratio for relationship in non_zero_relationships)

        if non_zero_total_ratio == 0:
            raise ValueError("No active team members with non-zero earning ratio.")

        for relationship in non_zero_relationships:
            ratio = relationship.earning_ratio
            earning = cls.transaction_amount * (ratio / non_zero_total_ratio)
            earnings[relationship.member] = earning

        if active_relationships.count() == 1:
            # Credit founder's account if there's only one active team member
            team_founder = team.team_founder
            team_founder.account_balance += cls.transaction_amount
            team_founder.save()
        else:
            remaining_amount = cls.transaction_amount - sum(earnings.values())
            if remaining_amount > 0:
                raise ValueError("Remaining amount cannot be distributed.")
            
            for member, earning in earnings.items():
                member.account_balance += earning
                member.save()

        return earnings


class TeamMember(models.Model):
    team = models.ForeignKey(Team, verbose_name=_("Team"), on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Team Member"), blank=True, on_delete=models.CASCADE)
    earning_ratio = models.PositiveIntegerField(_("Earning Ratio"), default=0)
    status = models.BooleanField(_("Active for Pay"), choices=((False, 'Cannot be Paid'), (True, 'Eligible for Pay')), default=True)

    @classmethod
    def create(cls, team, member, earning_ratio):
        return cls.objects.create(team=team, member=member, earning_ratio=earning_ratio)

    def __str__(self):
        return self.team.title


# this is for External User Invitations
class Invitation(MerchantMaster):
    # Type
    FOUNDER = 'founder'
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    TYPE = (
        (FOUNDER, _('Founder')),
        (INTERNAL, _('Internal')),
        (EXTERNAL, _('External'))
    )
    # Status
    INVITED = 'invited'
    ACCEPTED = 'accepted'
    STATUS = (
        (INVITED, _('Invited')),
        (ACCEPTED, _('Accepted'))
    )
    team = models.ForeignKey(Team, verbose_name=_("Team"), related_name='invitations', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name="sender", blank=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Receiver"), related_name="receiver", blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(_("Email"), max_length=100, blank=True)
    code = models.CharField(_("Code"), max_length=10, blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS, default=INVITED)
    type = models.CharField(_("Invite Type"), max_length=20, choices=TYPE, default=FOUNDER)
    sent_on = models.DateTimeField(_("Date"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = create_random_code()
        if self.merchant is None:
            self.merchant = self.team.merchant          
        super(Invitation, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


    @classmethod
    def founder_invitation(cls, team, type, status):
        internal_invite = cls.objects.create(
            team=team, 
            type=type, 
            sender=team.created_by, 
            email=team.created_by.email, 
            status=status,
            merchant = team.merchant
        )
        return internal_invite


    @classmethod
    def internal_invitation(cls, team, sender, type, receiver, email):

        if not team:
            raise InvitationException(_("Your team is unknown"))

        if not sender:
            raise InvitationException(_("Bad and unknown request"))

        if not receiver:
            raise InvitationException(_("credentials of invitee missing"))

        if not email:
            raise InvitationException(_("credentials of invitee missing"))

        if not (team.package_status == 'active'):
            raise InvitationException(_("Please upgrade your team to invite others"))

        if not (team.package.type == 'team'):
            raise InvitationException(_("Please activate subscription to invite others"))

        if team.created_by != sender:
            raise InvitationException(_("You must invite from your upgraded team"))

        if team.created_by == receiver:
            raise InvitationException(_("You cannot invite youself"))
        
        if Customer.objects.filter(user_type=Customer.CLIENT, email=email).exists():
            raise InvitationException(_("Owner is already a client and can't be invited"))
        
        if Customer.objects.filter(is_staff=True, email=email).exists():
            raise InvitationException(_("This user can't be invited"))
        
        if cls.objects.filter(team=team, receiver=receiver).exists():
            raise InvitationException(_("User already invited"))  

        if cls.objects.filter(team=team, team__members__email=email).exists():
            raise InvitationException(_("User already a member"))

        if cls.objects.filter(team=team, receiver__email=email).exists():
            raise InvitationException(_("User of this email already invited"))

        if receiver in team.members.all():
            raise InvitationException(_("User already a member"))

        if not (team.package.max_member_per_team > team.invitations.count()):
            raise InvitationException(_("Maximum invitation exceeded"))
        
        internal_invite = cls.objects.create(
            team=team, 
            sender=sender, 
            type=type, 
            receiver=receiver, 
            email=email,
            merchant=team.merchant
        )
        return internal_invite


    @classmethod
    def external_invitation(cls, team, sender, email, type):
        if not team:
            raise InvitationException(_("Your team is unknown"))

        if not sender:
            raise InvitationException(_("Bad and unknown request"))

        if not email:
            raise InvitationException(_("credential of invitee invalid"))

        if team.created_by.email == email:
            raise InvitationException(_("You cannot invite yourself"))

        if cls.objects.filter(team=team, team__members__email=email).exists():
            raise InvitationException(_("User already a member of your Team"))

        if cls.objects.filter(team=team, email=email).exists():
            raise InvitationException(_("Email User already invited"))

        if cls.objects.filter(team=team, receiver__email=email).exists():
            raise InvitationException(_("User of this email already invited"))

        if Customer.objects.filter(user_type=Customer.CLIENT, email=email).exists():
            raise InvitationException(_("Owner is already a client and can't be invited"))
        
        if Customer.objects.filter(is_staff=True, email=email).exists():
            raise InvitationException(_("This user can't be invited"))

        if not (team.package_status == 'active'):
            raise InvitationException(_("Please upgrade team to invite"))

        if not (team.package.type == 'team'):
            raise InvitationException(_("Please subscribe to invite others"))

        if team.created_by != sender:
            raise InvitationException(_("This action requires upgrade"))
          
        if not (team.package.max_member_per_team > team.invitations.count()):
            raise InvitationException(_("Maximum invitation exceeded"))

        external_invite = cls.objects.create(
            team=team, 
            sender=sender, 
            email=email, 
            type=type,
            merchant=team.merchant
        )
        return external_invite


class TeamChat(MerchantMaster):
    team = models.ForeignKey(Team, verbose_name=_("Chat Team"), related_name='teamchats', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='teamsender', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return self.content[:50] + '...'


class AssignMember(MerchantMaster):

    # Status
    TODO = 'todo'
    COMPLETED = 'completed'
    STATUS = (
        (TODO, 'Todo'),
        (COMPLETED, 'Completed'),
    )

    team = models.ForeignKey(Team, verbose_name=_("Team"), related_name='assignteam', on_delete=models.CASCADE)
    proposal = models.ForeignKey("proposals.Proposal",  verbose_name=_("Proposal"), related_name="assignproposal", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default=TODO)
    assignor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Assignor"), related_name="assignors", on_delete=models.CASCADE)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Assignee"), related_name='assignees', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified = models.DateTimeField(_("Assign On"), auto_now=True)
    duty = models.TextField(_("Job description"),max_length=500, blank=True, null=True)
    is_assigned = models.BooleanField(choices=((False, 'Unassigned'), (True, 'Assigned')), default=False)

    class Meta:
        ordering = ('-modified',)
        verbose_name = _("Assign Member")
        verbose_name_plural = _("Assign Member")


    def __str__(self):
        return f'{self.assignor.short_name} assign to {self.assignee.short_name}'

    def tracking_time(self):
        return sum(tracker.minutes for tracker in self.trackings.all())


class Tracking(MerchantMaster):
    team = models.ForeignKey(Team, verbose_name=_("Team"), related_name='trackings', on_delete=models.CASCADE)
    proposal = models.ForeignKey("proposals.Proposal",  verbose_name=_(
        "Proposal"), related_name="trackings", on_delete=models.CASCADE)
    assigned = models.ForeignKey(AssignMember, related_name='trackings', on_delete=models.CASCADE)
    tasks = models.TextField(_("Task description"),max_length=200, blank=True, null=True)
    is_tracked = models.BooleanField(choices=((False, 'untracked'), (True, 'Tracked')), default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Assignee"), related_name='trackings', on_delete=models.CASCADE)
    minutes = models.PositiveIntegerField(_("Time Tracked"), default=0)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.assigned.proposal.title
