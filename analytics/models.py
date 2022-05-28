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
        verbose_name = _("NewStats")
        verbose_name_plural = _("NewStats")

    def __str__(self):
        return self.description


class ProjectStatus(models.Model):
    description = models.CharField( _("Description"), default="Statistics data on project", max_length=100, null=True, blank=True)
    active = models.PositiveIntegerField(null=True, blank=True)
    review = models.PositiveIntegerField(null=True, blank=True)
    ongoing = models.PositiveIntegerField(null=True, blank=True)
    archived = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Projects Status")
        verbose_name_plural = _("Projects Status")

    def __str__(self):
        return f'self.project'


    # def save(self, *args, **kwargs):

    #     self.active = Project.objects.all().filter(status = Project.ACTIVE).count()
    #     self.review = Project.objects.all().filter(status = Project.REVIEW).count()
    #     self.ongoing = Project.objects.all().filter(status = Project.ONGOING).count()
    #     self.archived = Project.objects.all().filter(status = Project.ARCHIVED).count()    

    #     return super().save(*args, **kwargs)


    def active_count(self):
        self.active  = Project.objects.all().filter(status = Project.ACTIVE).count()       
        return self.active 

    def review_count(self):
        self.review  = Project.objects.all().filter(status = Project.REVIEW).count()
        return self.review 

    def ongoing_count(self):
        self.ongoing  = Project.objects.all().filter(status = Project.ONGOING).count()
        return self.ongoing 

    def archived_count(self):
        self.archived  = Project.objects.all().filter(status = Project.ARCHIVED).count()
        return self.archived 

# class ProjectStatus(models.Model):
#     description = models.CharField( _("Project Status"), default="Status of projects", max_length=100, null=True, blank=True)
#     total_ongoing_job = models.PositiveIntegerField()
#     total_completed_job = models.PositiveIntegerField()
#     total_cancelled_job = models.PositiveIntegerField()
#     android = models.PositiveIntegerField()
#     oth = models.PositiveIntegerField()



















