from email.mime import application
from django.db import models
from django.utils.translation import gettext_lazy as _
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
    #Below additional times apply to contract
    two_months,
    three_months,
    four_months,
    five_months,
    six_months
)


class ProjectResolution(models.Model):
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

    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedteam', on_delete=models.CASCADE)
    application = models.ForeignKey("transactions.ApplicationSale", verbose_name=_("Application"), related_name="projectapplicantsaction", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Offered"), related_name="resolutionproject", on_delete=models.CASCADE)

    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)


    def save(self, *args, **kwargs):

        if self.project.completion_time == self.ONE_DAY:
            self.end_time = one_day()
        elif self.project.completion_time == self.TWO_DAYS:
            self.end_time = two_days()
        elif self.project.completion_time == self.THREE_DAYS:
            self.end_time = three_days()
        elif self.project.completion_time == self.FOUR_DAYS:
            self.end_time = four_days()
        elif self.project.completion_time == self.FIVE_DAYS:
            self.end_time = five_days()
        elif self.project.completion_time == self.SIX_DAYS:
            self.end_time = six_days()
        elif self.project.completion_time == self.ONE_WEEK:
            self.end_time = one_week()
        elif self.project.completion_time == self.TWO_WEEK:
            self.end_time = two_weeks()
        elif self.project.completion_time == self.THREE_WEEK:
            self.end_time = three_weeks()
        elif self.project.completion_time == self.ONE_MONTH:
            self.end_time = one_month()
        super(ProjectResolution, self).save(*args, **kwargs)

        
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.team.title} vrs. {self.project.created_by.get_full_name()}'

# Also a review table required
class ProjectCancelation(models.Model):
    pass