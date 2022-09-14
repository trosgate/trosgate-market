from datetime import datetime
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from uuid import uuid4
from django.template.defaultfilters import slugify
from datetime import datetime, timezone, timedelta
from teams.utilities import create_random_code
from django.template.defaultfilters import truncatechars


class Application(models.Model):
    # Project Duration
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
    ESTIMATED_DURATION = (
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

    # Application Status
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    APPLICATION_STATUS = (
        (PENDING, _('Pending')),
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected')),
    ) 
    team = models.ForeignKey('teams.Team', verbose_name=_("Applicant Team"), related_name="applications", on_delete=models.CASCADE, max_length=250)
    project = models.ForeignKey('projects.Project', verbose_name=_("Project"), related_name="applications", on_delete=models.CASCADE)
    message = models.TextField(_("Message"), max_length=2000, null=True, blank=True)
    budget = models.IntegerField(_("Budget"), default=5, validators=[MinValueValidator(5), MaxValueValidator(50000)], error_messages={"name": {"max_length": _("Set the budget amount (Eg.1000) excluding the currency sign")}},)
    estimated_duration = models.CharField(_("Est. Duration"), max_length=20, choices=ESTIMATED_DURATION)    
    created_at = models.DateTimeField(auto_now_add=True)
    applied_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Applicant"),  related_name="applicants", on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=20, choices=APPLICATION_STATUS, default=PENDING)
 
    def __str__(self):
        return f'{self.project.title}'


    @property
    def message_slice(self):
        return truncatechars(self.message, 50)


    #a url route to view application detail page
    def get_application_detail_absolute_url(self):
        return reverse('applications:application_detail', args=[self.project.slug])

    #a url route to view application detail page
    def get_apply_for_project_absolute_url(self):
        return reverse('applications:apply_for_project', args=[self.slug])