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

# from freelancer.models import FreelancerAccount


def code_generator():
    generated_code = secrets.token_urlsafe(6)[:6]
    similar_ref = Invitation.objects.filter(code=generated_code)
    while not similar_ref:
        code = generated_code
        break
    return code


# team should have ability to add proposal extras
class Team(models.Model):
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
        (DEFAULT, 'Default'),
        (ACTIVE, 'Active')
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Team Founder"), related_name="teammanager", on_delete=models.CASCADE)
    merchant = models.ForeignKey('account.Merchant', verbose_name=_('Merchant'), related_name='teammerchant', on_delete=models.PROTECT)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Team Members"), related_name="team_member")
    
    title = models.CharField(_("Title"), max_length=100, unique=True)
    notice = models.TextField(_("Notice"), max_length=500)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    status = models.CharField(_("Team Status"), max_length=20, choices=STATUS, default=INACTIVE)
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

    @classmethod
    def add_new_team(cls, title, created_by, package, notice=None):
        with db_transaction.atomic():
            team = cls.objects.create(
                title=title,
                created_by=created_by,
                package=package,
                notice=notice
            )
            team.members.add(team.created_by)
        return team

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)            
        super(Team, self).save(*args, **kwargs)


# this is for External User Invitations
class Invitation(models.Model):
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
    merchant = models.ForeignKey('account.Merchant', verbose_name=_('Merchant'), related_name='merchantinvite', on_delete=models.PROTECT)
    team = models.ForeignKey(Team, verbose_name=_("Team"), related_name='invitations', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name="sender", blank=True, on_delete=models.PROTECT) #CASCADE
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Receiver"), related_name="receiver", blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(_("Email"), max_length=100, blank=True)
    code = models.CharField(_("Code"), max_length=10, blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS, default=INVITED)
    type = models.CharField(_("Invite Type"), max_length=20, choices=TYPE, default=FOUNDER)
    sent_on = models.DateTimeField(_("Date"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = create_random_code()          
        super(Invitation, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


    @classmethod
    def new_team_and_invitation(cls, current_team, created_by, title, package, type, status, notice=None):
        with db_transaction.atomic():

            if notice is None:
                notice= ''    

            if not (current_team.created_by == created_by):
                raise InvitationException(_("You must be in your founded team to create new Teams"))

            new_team = Team.add_new_team(
                title=title, created_by=created_by, package=package,notice=notice
            )
            new_team.status = 'active'
            new_team.save()

            internal_invite = cls.objects.create(
                team=new_team, type=type, sender=new_team.created_by, email=new_team.created_by.email, status=status
            )
        return new_team, internal_invite


    @classmethod
    def internal_invitation(cls, team, sender, type, receiver, email):

        if not team:
            raise InvitationException(_("Your team is unknown"))

        if not sender:
            raise InvitationException(_("Bad and unknown request"))

        if not receiver:
            raise InvitationException(_("credentials of invitee incomplete"))

        if not email:
            raise InvitationException(_("credentials of invitee incomplete"))

        if not (team.package_status == 'active'):
            raise InvitationException(_("Please upgrade your team to invite others"))

        if not (team.package.type == 'Team'):
            raise InvitationException(_("Please activate subscription to invite others"))

        if team.created_by != sender:
            raise InvitationException(_("This action requires upgraded team founder"))

        if team.created_by == receiver:
            raise InvitationException(_("You cannot invite youself"))

        if cls.objects.filter(team=team, receiver=receiver).exists():
            raise InvitationException(_("User already invited"))     

        if cls.objects.filter(team=team, team__members__email=email).exists():
            raise InvitationException(_("User already a member of your Team"))

        if cls.objects.filter(team=team, receiver__email=email).exists():
            raise InvitationException(_("User of this email already invited"))

        if receiver in team.members.all():
            raise InvitationException(_("User already a member"))

        internal_invite = cls.objects.create(team=team, sender=sender, type=type, receiver=receiver, email=email)
        return internal_invite


    @classmethod
    def external_invitation(cls, team, sender, email, type):
        #TODO Check for maximum number of members
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
            raise InvitationException(_("Email owner is already a client and can't be invited"))
        
        if Customer.objects.filter(user_type=Customer.ADMIN, email=email).exists():
            raise InvitationException(_("This Email user is reserved and can't be invited"))

        if not (team.package_status == 'active'):
            raise InvitationException(_("Please upgrade your team to invite others"))

        if not (team.package.type == 'Team'):
            raise InvitationException(_("Please subscribe to invite others"))

        if team.created_by != sender:
            raise InvitationException(_("This action requires upgraded team founder"))

        external_invite = cls.objects.create(team=team, sender=sender, email=email, type=type)
        return external_invite


class TeamChat(models.Model):
    team = models.ForeignKey(Team, verbose_name=_("Chat Team"), related_name='teamchats', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='teamsender', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return self.content[:50] + '...'


class AssignMember(models.Model):

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


class Tracking(models.Model):
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
