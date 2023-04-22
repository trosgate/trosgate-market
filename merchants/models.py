from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.urls import reverse
from django_cryptography.fields import encrypt
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


# managers.py
from django.db import models


class MerchantMasterManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        site = Site.objects.get_current()
        return qs.filter(merchant=site.id)

class UnscopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class MerchantMaster(models.Model):
    merchant = models.ForeignKey("account.Merchant", verbose_name=_("Merchant"), on_delete=models.PROTECT)
    
    objects = MerchantMasterManager()
    allobjects = UnscopedManager()
    
    class Meta:
        abstract = True


class MerchantProduct(models.Model):
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
    MODIFY = 'modify' # should be ongoing for projects
    ARCHIVE = 'archived'
    STATUS = (
        (REVIEW, _("Review")),
        (ACTIVE, _("Active")),
        (MODIFY, _("Modify")),
        (ARCHIVE, _("Archived")),
    )    
    merchant = models.ForeignKey("account.Merchant", verbose_name=_("Merchant"), on_delete=models.PROTECT)
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    category = models.ForeignKey('general_settings.Category', verbose_name=_("Category"), on_delete=models.RESTRICT, max_length=250)
    slug = models.SlugField(_("Slug"), max_length=255)
    preview = models.CharField(_("Preview"), max_length=255, error_messages={"name": {"max_length": _("Preview field is required with maximum of 250 characters")}},)
    skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("Proposal Skills"),  error_messages={"name": {"max_length": _("Skill field is required")}},)
    sample_link = models.URLField(_("Sample Website"), max_length=2083, help_text=_("the link must be a verified url"), null=True, blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS, default=REVIEW)
    description = models.TextField(verbose_name=_("Description"), max_length=3500, error_messages={"name": {"max_length": _("Description field is required")}},)
    dura_converter = models.CharField(_("Deadline"), max_length=100, choices=DURATION_CONVERTER, default = ONE_DAY)    
    service_level = models.CharField(_("Service Level"), max_length=20, choices=SERVICE_LEVEL, default=BASIC, error_messages={"name": {"max_length": _("Service Level field is required")}},)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), on_delete=models.CASCADE)
    reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
    published = models.BooleanField(_("Featured"), choices = ((False,'Unfeature'), (True, 'Feature')), default = False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    salary = models.IntegerField(_("Price"), default=10, validators=[MinValueValidator(10), MaxValueValidator(50000)], error_messages={"amount": {"max_length": _("Set the budget amount between 10 and 50000 currency points")}},)       

    objects = MerchantMasterManager()
    allobjects = UnscopedManager()
    
    class Meta:
        abstract = True