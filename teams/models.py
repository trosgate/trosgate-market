from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from django.core.mail import send_mail
from . utilities import send_invitation_email, create_random_code, send_new_team_email
from django.core.exceptions import ValidationError
from uuid import uuid4


# NB ---> create seperate status for each of the fields and display to users
class Package(models.Model):
    #
    # Team statuses
    STARTER = 'starter'
    STANDARD = 'standard'
    LATEST = 'latest'
    STATUS = (
        (STARTER, _('Starter')),
        (STANDARD, _('Standard')),
        (LATEST, _('Latest')),
    )

    #
    # Initial Plan Configuration
    type = models.CharField(_("Package Type"), unique=True, help_text=_(
        "package type can be eg. BASIC"), max_length=50)
    verbose_type = models.CharField(_("Branded Name"), unique=True, blank=True, null=True, help_text=_(
        "Customize name for the package. If empty, the default names will be displayed"), max_length=50)
    max_member_per_team = models.PositiveIntegerField(_("Max member Per Team"), default=1, help_text=_(
        "You can only add up to 4 members for the biggest package"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    monthly_offer_contracts_per_team = models.PositiveIntegerField(_("Monthly Offer Contracts Per Team"), default=0, help_text=_(
        "Clients can view team member's profile and send offer Contracts up to 100 monthly"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_proposals_allowable_per_team = models.PositiveIntegerField(_("Max Proposals Per Team"), default=5, help_text=_(
        "You can add min of 5 and max of 50 Proposals per Team"), validators=[MinValueValidator(5), MaxValueValidator(50)])
    monthly_projects_applicable_per_team = models.PositiveIntegerField(_("Max Job/Project Applicable Per Team"), default=10, help_text=_(
        "Monthly Jobs Applications with min of 5 and max 50"), validators=[MinValueValidator(5), MaxValueValidator(50)])
    daily_Handshake_mails_to_clients = models.PositiveIntegerField(_("Daily Handshake Mails Per Invoice to client"), default=0, help_text=_(
        "team can send followup mail per invoice to client. Daily min is 1 amd max is 3"), validators=[MinValueValidator(1), MaxValueValidator(3)])
    price = models.PositiveIntegerField(_("Package Price"), default=0, help_text=_(
        "Decide your reasonable price with max limit of 1000"), validators=[MinValueValidator(0), MaxValueValidator(1000)])
    status = models.CharField(
        _("Package Label"), max_length=20, choices=STATUS, default=STARTER)
    is_default = models.BooleanField(_("Make Default"), choices=((False, 'No'), (True, 'Yes')), help_text=_(
        "Only 1 package should have a default set to 'Yes'"), default=False)
    ordering = models.PositiveIntegerField(_("Display"), default=1, help_text=_(
        "This determines how each package will appear to user eg, 1 means first position"), validators=[MinValueValidator(1), MaxValueValidator(3)])

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['ordering']


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

    title = models.CharField(_("Title"), max_length=100, unique=True)
    notice = models.TextField(_("Notice"), max_length=500)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "Team Members"), related_name="team_member")
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Team Founder"), related_name="teammanager", on_delete=models.CASCADE)
    status = models.CharField(
        _("Team Status"), max_length=20, choices=STATUS, default=ACTIVE)
    package = models.ForeignKey(
        Package, related_name='teams', on_delete=models.CASCADE)
    package_status = models.CharField(
        _("Package Status"), max_length=20, choices=PACKAGE_STATUS, default=DEFAULT)
    package_expiry = models.DateTimeField(
        _("Package Expiry Date"), blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=100, editable=True)
    # payment method to be used by User to activate plan
    stripe_customer_id = models.CharField(
        _("Stripe Customer ID"), max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(
        _("Stripe Subscription ID"), max_length=255, blank=True, null=True)
    paypal_customer_id = models.CharField(
        _("Paypal Customer ID"), max_length=255, blank=True, null=True)
    paypal_subscription_id = models.CharField(
        _("Paypal Subscription ID"), max_length=255, blank=True, null=True)

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

    # def member_indexing(self):
    #     members = self.members.all()
    #     for index, member in enumerate(members, start=1):
    #         member.index = index
    #         print(member.index, member.short_name)
            # yield member


# this is for External User Invitations
class Invitation(models.Model):
    #
    # Status

    INVITED = 'invited'
    ACCEPTED = 'accepted'

    STATUS = (
        (INVITED, _('Invited')),
        (ACCEPTED, _('Accepted'))
    )

    team = models.ForeignKey(
        Team, related_name='invitations', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    code = models.CharField(unique=True, max_length=10, blank=True,)
    status = models.CharField(max_length=20, choices=STATUS, default=INVITED)
    sent_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = create_random_code()[:6]
        super(Invitation, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class TeamChat(models.Model):
    team = models.ForeignKey(Team, verbose_name=_(
        "Chat Team"), related_name='teamchats', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Sender"), related_name='teamsender', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return self.content[:50] + '...'

    # def get_team_activated_url(self):
    #       return reverse('teams:team_chat', args=[self.id])


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
    duty = models.TextField(_("Job description"),max_length=500, blank=True, null=True)
    is_assigned = models.BooleanField(choices=((False, 'Unassigned'), (True, 'Assigned')), default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Assign Member")
        verbose_name_plural = _("Assign Member")
        # unique_together = ("proposal", "assignee")

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
