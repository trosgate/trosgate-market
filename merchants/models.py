from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.sites.models import Site
from account.models import Merchant
import uuid
from django.contrib.sites.managers import CurrentSiteManager


    
class MerchantMasterManager(models.Manager):
    def get_queryset(self):
        current_site = Site.objects.get_current()
        qs = super().get_queryset()
        if current_site.pk == 1:
            queryset = qs
        else:
            queryset = qs.filter(merchant__site=current_site)
        return queryset
        


class MerchantMaster(models.Model):
    merchant = models.ForeignKey("account.Merchant", verbose_name=_("Merchant"), on_delete=models.PROTECT)
    objects = MerchantMasterManager()
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        current_site = Site.objects.get_current()
        if not self.merchant_id:
            self.merchant=Merchant.objects.filter(site=current_site).first()
        super().save(*args, **kwargs)


class MerchantProduct(MerchantMaster):
    ONE_DAY = 1
    TWO_DAYS = 2
    THREE_DAYS = 3
    FOUR_DAYS = 4
    FIVE_DAYS = 5
    SIX_DAYS = 6
    ONE_WEEK = 7
    TWO_WEEK = 14
    THREE_WEEK = 21
    ONE_MONTH = 30
    PACKAGE_DURATION = (
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

    ONE_TIME = 1
    TWO_TIMES = 2
    THREE_TIMES = 3
    FOUR_TIMES = 4
    FIVE_TIMES = 5
    SIX_TIMES = 6
    SEVEN_TIMES = 7
    REVISION_CHOICES = (
        (ONE_TIME, _("1 Time")),
        (TWO_TIMES, _("2 Times")),
        (THREE_TIMES, _("3 Times")),
        (FOUR_TIMES, _("4 Times")),
        (FIVE_TIMES, _("5 Times")),
        (SIX_TIMES, _("6 Times")),
        (SEVEN_TIMES, _("7 Times")),
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
    # Product Status
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
    id = models.AutoField(primary_key=True),
    identifier = models.URLField(editable=False, unique=True, default=uuid.uuid4, verbose_name='Identifier')    
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    category = models.ForeignKey('general_settings.Category', verbose_name=_("Category"), on_delete=models.RESTRICT, max_length=250)
    slug = models.SlugField(_("Slug"), max_length=255)
    preview = models.CharField(_("Preview"), max_length=255, error_messages={"name": {"max_length": _("Preview field is required with maximum of 250 characters")}},)
    skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("Proposal Skills"),  error_messages={"name": {"max_length": _("Skill field is required")}},)
    sample_link = models.URLField(_("Sample Website"), max_length=2083, help_text=_("the link must be a verified url"), null=True, blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS, default=ACTIVE)
    description = models.TextField(verbose_name=_("Description"), max_length=3500, error_messages={"name": {"max_length": _("Description field is required")}},)
    service_level = models.CharField(_("Service Level"), max_length=20, choices=SERVICE_LEVEL, default=BASIC, error_messages={"name": {"max_length": _("Service Level field is required")}},)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), on_delete=models.CASCADE)
    reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
    published = models.BooleanField(_("Featured"), choices = ((False,'Unfeature'), (True, 'Feature')), default = False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    salary = models.IntegerField(_("Price"), error_messages={"amount": {"max_length": _("Set the salary for this proposal")}},)       
    revision = models.PositiveIntegerField(_("Revision"), choices=REVISION_CHOICES, default=ONE_TIME)    
    duration = models.PositiveIntegerField(_("Duration"), choices=PACKAGE_DURATION, default=THREE_DAYS)
    duration_time = models.DateTimeField(_("Duration Time"), null=True, blank=True, help_text=_("deadline for expiration of project"))

    class Meta:
        abstract = True







































