from django.db import models
from django.utils.translation import gettext_lazy as _
from projects.models import Project
from django.db.models import F
from projects . models import Project
from django.db.models import Count


class NewStats(models.Model):
    description = models.CharField( _("NewStats"), default="Statistics data on website visitors", max_length=100, null=True, blank=True)
    win = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    mac = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    iph = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    android = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    oth = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))


    class Meta:
        verbose_name = _("Visitor Stats")
        verbose_name_plural = _("Visitor Stats")

    def __str__(self):
        return self.description

















