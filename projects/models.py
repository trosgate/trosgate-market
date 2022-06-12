
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
    two_months,
    three_months,
    four_months,
    five_months,
    six_months
)


class ProjectLanguageRequired(models.Model):
    # level_of_proficiency
    BASIC = 'basic'
    STANDARD = 'standard'
    EXPERT = 'expert'
    USER_SKILL_LEVEL = (
        (BASIC, _('Basic')),
        (STANDARD, _('Standard')),
        (EXPERT, _('expert')),
    )  
   
    project_language = models.CharField(_("Project Language"),max_length=30)
    language = models.ForeignKey('general_settings.CommunicationLanguage', verbose_name=_("Language"), on_delete=models.CASCADE)
    level_of_proficiency = models.CharField(max_length=30, choices=USER_SKILL_LEVEL, default=BASIC, help_text=_("Please select as appropriate"))

    class Meta:
        verbose_name = _("Project Language")
        verbose_name_plural = _("Project Language")

    def __str__(self):
        return self.project_language


class Project(models.Model):
    # Service Level
    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'
    SERVICE_LEVEL = (
        (BASIC, _('Basic')),
        (STANDARD, _('Standard')),
        (PREMIUM, _('Premium')),
    )  

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
    PROJECT_DURATION = (
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
     
    #status  
    REVIEW = 'review'
    ACTIVE = 'active'
    ONGOING = 'ongoing'
    ARCHIVED = 'archived'
    STATUS = (
        (REVIEW, _("Review")),
        (ACTIVE, _("Active")),
        (ONGOING, _("Ongoing")),
        (ARCHIVED, _("Archived")),
    )

    RATINGS = (
        (0, "☆☆☆☆☆"),
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

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

    category = models.ForeignKey('general_settings.Category', verbose_name=_("Category"),  related_name="projects", on_delete=models.RESTRICT, error_messages={"name": {"max_length": _("You need to set category before projects can be created")}},)
    title = models.CharField(_("Title"), max_length=255, help_text=_("Title field is Required"), unique=True, error_messages={"name": {"max_length": _("Title field must be unique for your individual projects")}},)
    slug = models.SlugField(_("Slug"), max_length=255)
    preview = models.TextField(_("Preview"), max_length=250, error_messages={"name": {"max_length": _("Preview field is required")}},)
    description = RichTextField(_("Description"), max_length=3500, error_messages={"name": {"max_length": _("Describe your proposal in details")}},)
    service_level = models.CharField(_("Service Level"), max_length=20, choices=SERVICE_LEVEL, default=BASIC, error_messages={"name": {"max_length": _("Service Level field is required")}},)
    sample_link = models.URLField(_("Sample Website"), max_length=2083, help_text=_("the link must be a verified url"),null=True,blank=True)
    project_skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("Project Skill"))
    rating = models.PositiveSmallIntegerField(_("Rating"), choices=RATINGS, default=0)
    amount = models.IntegerField(_("Budget"), default=5, validators=[MinValueValidator(5), MaxValueValidator(50000)], error_messages={"name": {"max_length": _("Set the budget amount (eg.1000) excluding the currency sign")}},)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    dura_converter = models.CharField(_("Duration"), max_length=100, choices=PROJECT_DURATION, default = ONE_DAY)
    duration = models.DateTimeField(_("Deadline"), blank=True, help_text=_("deadline for project"))
    completion_time = models.CharField(_("Completion In"), max_length=100, choices=PROJECT_COMPLETION, default = ONE_DAY)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Project Author"), related_name="project", on_delete=models.CASCADE)
    published = models.BooleanField(_("Featured"), choices = ((False,'Unfeature'), (True, 'Feature')), default = False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS, default=REVIEW)
    reference = models.CharField(_('Identifier'), unique=True, null=True, blank=True, max_length=120)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.reference is None:
            self.reference = 'Pj-' + str(uuid4()).split('-')[4]
        # if self.dura_converter == self.ONE_DAY:
        #     self.duration = one_day()
        # if self.dura_converter == self.TWO_DAYS:
        #     self.duration = two_days()
        # if self.dura_converter == self.THREE_DAYS:
        #     self.duration = three_days()
        # if self.dura_converter == self.FOUR_DAYS:
        #     self.duration = four_days()
        # if self.dura_converter == self.FIVE_DAYS:
        #     self.duration = five_days()
        # if self.dura_converter == self.SIX_DAYS:
        #     self.duration = six_days()
        # if self.dura_converter == self.ONE_WEEK:
        #     self.duration = one_week()
        # if self.dura_converter == self.TWO_WEEK:
        #     self.duration = two_weeks()
        # if self.dura_converter == self.THREE_WEEK:
        #     self.duration = three_weeks()
        # if self.dura_converter == self.ONE_MONTH:
        #     self.duration = one_month()
        super(Project, self).save(*args, **kwargs)


    #a url route for the project detail page
    def get_project_absolute_url(self):
          return reverse('projects:project_detail', args=[self.slug])

    #a url route for the project update page
    def get_project_update_absolute_url(self):
        return reverse('projects:update_project', args=[self.slug])

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

    # def get_discount(self):
    #     discounts = 0
    #     for discount in self.applicantprojectapplied.all():
    #         discounts = discount.discount_offered
    #     return discounts



class ProjectSkillRequired(models.Model):
    # level_of_proficiency
    BASIC = 'basic'
    STANDARD = 'standard'
    EXPERT = 'expert'
    USER_SKILL_LEVEL = (
        (BASIC, _('Basic')),
        (STANDARD, _('Standard')),
        (EXPERT, _('expert')),
    ) 
    project = models.ForeignKey(Project,  verbose_name=_("Project"), related_name="projectskill", on_delete=models.CASCADE)
    skill = models.ManyToManyField('general_settings.Skill', verbose_name=_("Skill"))
    level_of_proficiency = models.CharField(_("Proficiency level"), max_length=30, choices=USER_SKILL_LEVEL, default=BASIC, help_text=_("Please select as appropriate"))

    class Meta:
        verbose_name = _("Project Skill")
        verbose_name_plural = _("Project Skills")

    def __str__(self):
        return self.level_of_proficiency
