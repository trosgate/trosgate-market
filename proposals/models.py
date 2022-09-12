from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from uuid import uuid4
from teams.utilities import create_random_code
from datetime import datetime, timezone, timedelta
from general_settings.storage_backend import activate_storage_type, DynamicStorageField


def proposal_images_path(instance, filename):
    return "proposal/%s/%s" % (instance.team.title, filename)


class ActiveProposals(models.Manager):
    def get_queryset(self):
        return super(ActiveProposals, self).get_queryset().filter(status=Proposal.ACTIVE)


class Proposal(models.Model):
    STORAGE = activate_storage_type()
    # proposal Duration converter
    ONE_DAY = "one_day"
    TWO_DAYS = "two_days"
    THREE_DAYS = "three_days"
    FOUR_DAYS = "four_days"
    FIVE_DAYS = "five_days"
    SIX_DAYS = "six_days"
    ONE_WEEK = "one_week"
    TWO_WEEK = "two_weeks"
    THREE_WEEK = "three_weeks"
    ONE_MONTH = "one_month"
    DURATION_CONVERTER = (
        (ONE_DAY, _("01 Day")),
        (TWO_DAYS, _("02 Days")),
        (THREE_DAYS, _("03 Days")),
        (FOUR_DAYS, _("04 Days")),
        (FIVE_DAYS, _("05 Days")),
        (SIX_DAYS, _("06 Days")),
        (ONE_WEEK, _("01 Week")),
        (TWO_WEEK, _("02 Weeks")),
        (THREE_WEEK, _("03 Weeks")),
        (ONE_MONTH, _("01 Month")),
    )

    # Service Level
    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'
    SERVICE_LEVEL = (
        (BASIC, _('Basic')),
        (STANDARD, _('Standard')),
        (PREMIUM, _('Premium')),
    )
    #
    # Proposal Status
    REVIEW = 'review'
    ACTIVE = 'active'
    MODIFY = 'modify'
    ARCHIVE = 'archived'
    STATUS = (
        (REVIEW, _("Review")),
        (ACTIVE, _("Active")),
        (MODIFY, _("Modify")),
        (ARCHIVE, _("Archived")),
    )
    #
    # Proposal Overview
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    category = models.ForeignKey('general_settings.Category', verbose_name=_("Category"), related_name="proposal", on_delete=models.RESTRICT, max_length=250)
    slug = models.SlugField(_("Slug"), max_length=255)
    preview = models.CharField(_("Preview"), max_length=255, error_messages={"name": {"max_length": _("Preview field is required with maximum of 250 characters")}},)
    skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("Proposal Skills"),  error_messages={"name": {"max_length": _("Skill field is required")}},)
    sample_link = models.URLField(_("Sample Website"), max_length=2083, help_text=_("the link must be a verified url"), null=True, blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS, default=REVIEW)
    # Main body content
    description = RichTextField(verbose_name=_("Description"), max_length=3500, error_messages={"name": {"max_length": _("Description field is required")}},)
    faq_one = models.CharField(_("FAQ #1"), max_length=100)
    faq_one_description = models.TextField(_("FAQ #1 Details"), max_length=255)
    faq_two = models.CharField(_("FAQ #2"), max_length=100, null=True, blank=True)
    faq_two_description = models.TextField(_("FAQ #2 Details"), max_length=255, null=True, blank=True)
    faq_three = models.CharField(_("FAQ #3"), max_length=100, null=True, blank=True)
    faq_three_description = models.TextField(_("FAQ #3 Details"), max_length=255, null=True, blank=True)
    # proposal summary
    salary = models.PositiveIntegerField(_("Salary"), default=10, help_text=_("Minimum Salary is $10"), validators=[MinValueValidator(10), MaxValueValidator(50000)])
    service_level = models.CharField(_("Service level"), max_length=20, choices=SERVICE_LEVEL, default=BASIC, error_messages={"name": {"max_length": _("Service Level field is required")}},)
    revision = models.BooleanField(_("Revision"), choices=((False, 'No'), (True, 'Yes')), default=False)
    dura_converter = models.CharField(_("Duration"), max_length=100, choices=DURATION_CONVERTER, default=ONE_DAY)
    thumbnail = models.ImageField(_("Thumbnail"), help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to=proposal_images_path, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    progress = models.PositiveIntegerField(_("% Progress"), default=0, help_text=_("Proposal Progress"), validators=[MinValueValidator(10), MaxValueValidator(50000)])
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    published = models.BooleanField(_("Published"), choices=((False, 'Private'), (True, 'Public')), default=False)
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="proposalteam", on_delete=models.CASCADE, max_length=250)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="proposalauthor", on_delete=models.CASCADE)
    reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
    objects = models.Manager()
    active = ActiveProposals()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Proposal")
        verbose_name_plural = _("Proposals")

    def __str__(self):
        return f'{self.title} - (Amount={self.salary}, Duration={self.get_dura_converter_display()})'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.thumbnail))

    image_tag.short_description = 'thumbnail'

    def tracking_time(self):
        return sum(tracker.minutes for tracker in self.trackings.all())

    def save(self, *args, **kwargs):
        super(Proposal, self).save(*args, **kwargs)
        # if self.thumbnail:
        #     new_thumbnail = Image.open(self.thumbnail.path)
        #     if new_thumbnail.height > 769 or new_thumbnail.width > 1280:
        #         output_size = (769, 1280)
        #         new_thumbnail.thumbnail(output_size)
        #         new_thumbnail.save(self.thumbnail.path)


    def percent_progress(self):
        return f'{self.progress}%'



class ProposalSupport(Proposal):
    class Meta:
        proxy=True
        ordering = ['created_at']
        verbose_name = _("Proposal Support")
        verbose_name_plural = _("Proposal Support")


class ProposalChat(models.Model):
    team = models.ForeignKey('teams.Team', verbose_name=_("Proposal Team"), related_name='proposalchats', on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, verbose_name=_("Proposal"), related_name='proposalschats', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='proposalsender', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return f'Message sent by {self.sender.get_full_name()}'






















