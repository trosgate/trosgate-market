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
from teams.utilities import create_random_code
from django.template.defaultfilters import truncatechars
from proposals.utilities import (
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
)
from merchants.models import MerchantProduct


class PublishedProjects(models.Manager):
    def get_queryset(self):
        return super(PublishedProjects, self).get_queryset().filter(published=True, status='active', duration__gte=timezone.now())


class Project(MerchantProduct):
    RATINGS = (
        (0, "☆☆☆☆☆"),
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

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
    PROJECT_COMPLETION = (
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
    sample_link = models.URLField(_("Sample Website"), max_length=2083, help_text=_("the link must be a verified url"),null=True,blank=True)
    rating = models.PositiveSmallIntegerField(_("Rating"), choices=RATINGS, default=0)
    duration = models.DateTimeField(_("Duration"), null=True, blank=True, help_text=_("deadline for expiration of project"))
    completion_time = models.CharField(_("Completion In"), max_length=100, choices=PROJECT_COMPLETION, default = ONE_DAY)
    action = models.BooleanField(_("Action"), default = False)
    reopen_count = models.PositiveSmallIntegerField(_("Reopen Count"), default=0, validators=[MinValueValidator(0), MaxValueValidator(1)],)
    objects = models.Manager()
    public = PublishedProjects()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.duration is None:
            self.duration=timezone.now()
        if self.reference is None:
            try:
                self.reference = 'P' + str(uuid4()).split('-')[4]
            except:
                self.reference = 'P' + str(uuid4()).split('-')[4]
        super(Project, self).save(*args, **kwargs)


    #a url route for the project detail page
    def get_project_absolute_url(self):
          return reverse('projects:project_detail', args=[self.slug])

    #a url route for the project update page
    def get_project_review_absolute_url(self):
        return reverse('projects:review_project', args=[self.slug])

    #a url route for the archive project page
    def get_project_archive_view_absolute_url(self):
        return reverse('projects:archived_project', args=[self.slug])

    #a url route to change active project to archived project
    def get_project_archive_absolute_url(self):
        return reverse('projects:archive_project', args=[self.slug])

    #a url route to change archived project to active project
    def get_project_archive_restored_absolute_url(self):
        return reverse('projects:restore_archive_project', args=[self.slug])

    def get_reopen_project_absolute_url(self):
        return reverse('projects:reopen_project', args=[self.slug])

