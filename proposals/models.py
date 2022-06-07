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
from .utilities import (
    one_day,
    two_days,
    three_days,
    four_days,
    five_days,
    six_days,
    one_week,
    two_weeks,
    three_weeks,
    one_month,
    two_months,
    three_months,
    four_months,
    five_months,
    six_months
)


# def proposal_images_path(instance, filename):
#     return f"proposal_image_{instance.pk}/{filename}"

def proposal_images_path(instance, filename):
    return "proposal/%s/%s" % (instance.team.title, filename)


class Proposal(models.Model):
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
    duration = models.DateTimeField(_("Completion In"), blank=True, help_text=_("duration for proposal task to be completed"))
    discount_price = models.PositiveIntegerField(_("Discount Price"), null=True, blank=True, default=5, help_text=_("discount price must be less than actual price"), validators=[MinValueValidator(5), MaxValueValidator(10000)])
    discount_code = models.CharField(_("Discount code"), null=True, blank=True, max_length=20, help_text=_("Discount code for customer"))
    # proposal files
    video = video = EmbedVideoField(_("Proposal Video"), max_length=2083, help_text=_("Paste Youtube or Vimeo url here"), null=True, blank=True,)
    thumbnail = models.ImageField(_("Proposal Thumbnail"), default='proposal_files/thumbnail.jpg', help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"),upload_to=proposal_images_path, blank=True, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    # size is "width x height"
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    published = models.BooleanField(_("Published"), choices=((False, 'Private'), (True, 'Public')), default=False)
    file_type = models.BooleanField(choices=((False, 'Show Video'), (True, 'Show Image')), default=False)
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="proposalteam", on_delete=models.CASCADE, max_length=250)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="proposalauthor", on_delete=models.CASCADE)
    reference = models.CharField(unique=True, null=True, blank=True, max_length=100)

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
        if self.reference is None:
            self.reference = 'Pp-' + str(uuid4()).split('-')[4]
            
        if self.dura_converter == self.ONE_DAY:
            self.duration = one_day()
        elif self.dura_converter == self.TWO_DAYS:
            self.duration = two_days()
        elif self.dura_converter == self.THREE_DAYS:
            self.duration = three_days()
        elif self.dura_converter == self.FOUR_DAYS:
            self.duration = four_days()
        elif self.dura_converter == self.FIVE_DAYS:
            self.duration = five_days()
        elif self.dura_converter == self.SIX_DAYS:
            self.duration = six_days()
        elif self.dura_converter == self.ONE_WEEK:
            self.duration = one_week()
        elif self.dura_converter == self.TWO_WEEK:
            self.duration = two_weeks()
        elif self.dura_converter == self.THREE_WEEK:
            self.duration = three_weeks()
        elif self.dura_converter == self.ONE_MONTH:
            self.duration = one_month()

        super(Proposal, self).save(*args, **kwargs)

    # def num_tasks_todo(self):
    #     return self.assignproposal.filter(status=Task.TODO).count()

    # def get_kt_thumbnail(self):
    #     if self.thumbnail:
    #         return self.thumbnail.url
    #     else:
    #         self.thumbnail = self.make_kt_thumbnail()
    #         self.save()
    #         return self.thumbnail.url

    # def make_kt_thumbnail(self, image, size=(300,200)):
    #     img = Image.open(image)
    #     img.convert('RGB')
    #     img.thumbnail(size)

    #     thumb_io = BytesIO()
    #     img.save(thumb_io, 'JPEG', quality=85)

    #     thumbnail=File(thumb_io, name=image.name)

    #     return thumbnail


# class OfferContract(models.Model):

class OfferContract(models.Model):
    # Invoice Duration
    ONE_DAY = "01 day"
    TWO_DAYS = "02 days"
    THREE_DAYS = "03 days"
    FOUR_DAYS = "04 days"
    FIVE_DAYS = "05 days"
    SIX_DAYS = "06 days"
    ONE_WEEK = "01 week"
    TWO_WEEK = "02 week"
    THREE_WEEK = "03 week"
    ONE_MONTH = "01 month"
    TWO_MONTH = "02 month"
    THREE_MONTH = "03 month"
    FOUR_MONTH = "04 month"
    FIVE_MONTH = "05 month"
    SIX_MONTH = "06 month"
    INVOICE_DURATION = (
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
        (TWO_MONTH, _("02 Months")),
        (THREE_MONTH, _("03 Months")),
        (FOUR_MONTH, _("04 Months")),
        (FIVE_MONTH, _("05 Months")),
        (SIX_MONTH, _("06 Months")),
    )
    #
    # Invoice States
    ACTIVE = 'active'
    OVERDUE = 'overdue'
    PAID = 'paid'
    STATUS = (
        (ACTIVE, _('Active')),
        (OVERDUE, _('Overdue')),
        (PAID, _('Paid')),
    )
    #

    proposal = models.ForeignKey(Proposal, verbose_name=_(
        "Proposal"), related_name="offercontract", on_delete=models.CASCADE)
    team = models.ForeignKey('teams.Team', verbose_name=_(
        "Team"), related_name="offercontract", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Creator"), null=True, blank=True, related_name="offercontract", on_delete=models.SET_NULL)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    payment_duration = models.CharField(
        choices=INVOICE_DURATION, default=ONE_DAY, max_length=20)
    status = models.CharField(choices=STATUS, default=ACTIVE, max_length=100)
    notes = models.TextField(null=True, blank=True, max_length=500)

    reference = models.CharField(
        unique=True, null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    line_one = models.CharField(
        _('Product/Service One'), max_length=120, default=None, blank=True, null=True)
    line_one_quantity = models.IntegerField(
        _('Quantity'), default=0, blank=True, null=True)
    line_one_unit_price = models.IntegerField(
        _('Unit Price'), default=0, blank=True, null=True)
    line_one_total_price = models.IntegerField(
        _('Total'), default=0, blank=True, null=True)

    line_two = models.CharField(
        'Product/Service Two', max_length=120, default=None, blank=True, null=True)
    line_two_quantity = models.IntegerField(
        _('Quantity'), default=0, blank=True, null=True)
    line_two_unit_price = models.IntegerField(
        _('Unit Price'), default=0, blank=True, null=True)
    line_two_total_price = models.IntegerField(
        _('Total'), default=0, blank=True, null=True)

    line_three = models.CharField(
        'Product/Service Three', max_length=120, default=None, blank=True, null=True)
    line_three_quantity = models.IntegerField(
        _('Quantity'), default=0, blank=True, null=True)
    line_three_unit_price = models.IntegerField(
        _('Unit Price'), default=0, blank=True, null=True)
    line_three_total_price = models.IntegerField(
        _('Total'), default=0, blank=True, null=True)

    line_four = models.CharField(
        'Product/Service Four', max_length=120, default=None, blank=True, null=True)
    line_four_quantity = models.IntegerField(
        _('Quantity'), default=0, blank=True, null=True)
    line_four_unit_price = models.IntegerField(
        _('Unit Price'), default=0, blank=True, null=True)
    line_four_total_price = models.IntegerField(
        _('Total'), default=0, blank=True, null=True)

    grand_total = models.IntegerField(
        _('Grand Total'), default=0, blank=True, null=True)
