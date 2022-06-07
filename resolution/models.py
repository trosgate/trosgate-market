from email.mime import application
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.template.defaultfilters import truncatechars


def application_file_directory(instance, filename):
    return "application/%s/%s" % (instance.application.team.title, filename)


class ProjectResolution(models.Model):
    '''
    We used signal to compare the project completion time and the default values below to obtain end_time
    '''
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

    #Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedteam', on_delete=models.CASCADE)
    application = models.ForeignKey("transactions.ApplicationSale", verbose_name=_("Application"), related_name="projectapplicantsaction", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Offered"), related_name="resolutionproject", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    
    completed = models.BooleanField(_("Completed"), choices=((False, 'Ongoing'), (True, 'Completed')), default=False)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 

    def __str__(self):
        return f'{self.team.title} vrs. {self.project.created_by.get_full_name()}'


class ProjectCompletionFiles(models.Model):
    application = models.ForeignKey(ProjectResolution, verbose_name=_("Project File"), related_name="applicantcompletionfiles", on_delete=models.CASCADE)
    attachment = models.FileField(_("Attachment"), help_text=_("image must be any of these 'jpeg','pdf','jpg','png','psd',"), upload_to=application_file_directory, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])])
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)


    def __str__(self):
        return f"{self.application.title}'s project is {self.completed}"


class ProjectResolutionReview(models.Model):
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='reviewsteam', on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Offered"), related_name="reviewproject", on_delete=models.CASCADE)
    application = models.ForeignKey(ProjectResolution, verbose_name=_("Applicant Review"), related_name="reviewapplication", on_delete=models.CASCADE)
    message = models.TextField(_("Message"), validators=[MinValueValidator(50), MaxValueValidator(500)])
    rating = models.PositiveSmallIntegerField(_("Rating"), default=3)
    status = models.BooleanField(_("Confirm Work"), choices=((False, 'Pending'), (True, 'Completed')))
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)


    class Meta:
        ordering = ("-created_at",)


    def __str__(self):
        return f'{self.message_slice}({self.status})'


    @property
    def message_slice(self):
        return truncatechars(self.message, 50)



# class ProjectCancelation(models.Model):
    #will have types choices 
    #eg.. team abandoned, team is rude 









