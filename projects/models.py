from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.template.defaultfilters import slugify
from teams.utilities import create_random_code
from django.template.defaultfilters import truncatechars
from merchants.models import MerchantProduct
from django.contrib.sites.models import Site
from datetime import timedelta
from django.utils import timezone
from teams.utilities import generate_unique_reference



class Project(MerchantProduct):
    RATINGS = (
        (0, "☆☆☆☆☆"),
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

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
    completion_time = models.PositiveIntegerField(_("Completion In"), choices=PROJECT_COMPLETION, default = ONE_DAY)
    action = models.BooleanField(_("Action"), default = False)
    reopen_count = models.PositiveSmallIntegerField(_("Reopen Count"), default=0)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        unique_together = ['slug', 'merchant']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.duration_time is None:
            self.duration_time = (timezone.now() + timedelta(days = self.duration))

        if not self.reference:
            self.reference = generate_unique_reference(Project)

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

