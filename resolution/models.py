from email.mime import application
from turtle import title
from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from account.fund_exception import ReviewException

# from django.utils import timezone

# self.last_updated = timezone.localtime(timezone.now())


def application_file_directory(instance, filename):
    return "application/%s/%s" % (instance.application.team.title, filename)

def proposal_file_directory(instance, filename):
    return "proposal/%s/%s" % (instance.application.team.title, filename)


class ProjectResolution(models.Model):
    '''
    We used signal to compare the project completion time and the default values below to obtain end_time
    '''
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

    #Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedteam', on_delete=models.CASCADE)
    application = models.ForeignKey("transactions.ApplicationSale", verbose_name=_("Application Accepted"), related_name="projectapplicantsaction", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Offered"), related_name="resolutionproject", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    
    completed = models.BooleanField(_("Completed"), choices=((False, 'Ongoing'), (True, 'Completed')), default=False)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Application Approved")
        verbose_name_plural = _("Application Approved")


    def __str__(self):
        return f'{self.team.title} vrs. {self.project.created_by.get_full_name()}'



class ProjectCompletionFiles(models.Model):
    application = models.ForeignKey(ProjectResolution, verbose_name=_("Project File"), related_name="applicantcompletionfiles", on_delete=models.CASCADE)
    attachment = models.FileField(_("Attachment"), help_text=_("image must be any of these 'jpeg','pdf','jpg','png','psd',"), upload_to=application_file_directory, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])])
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Project File")
        verbose_name_plural = _("Project Files")


    def __str__(self):
        return self.application.team.title


class ApplicationReview(models.Model):
    resolution = models.ForeignKey(ProjectResolution, verbose_name=_("Applicant Review"), related_name="reviewapplication", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=100)
    message = models.TextField(_("Message"), max_length=650)
    rating = models.PositiveSmallIntegerField(_("Rating"), default=3)
    status = models.BooleanField(_("Confirm Work"), choices=((False, 'Pending'), (True, 'Completed')))
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)


    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Project Review")
        verbose_name_plural = _("Project Review")


    def __str__(self):
        return self.title




# class ProjectCancelation(models.Model):
    #will have types choices 
    #eg.. team abandoned, team is rude 


class ProposalResolution(models.Model):
    '''
    We used signal to compare the proposal completion time and the default values below to obtain end_time
    '''
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

    #Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedproposalteam', on_delete=models.CASCADE)
    proposal_sale = models.ForeignKey("transactions.ProposalSale", verbose_name=_("Proposal Sold"), related_name="proposalaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)   
    completed = models.BooleanField(_("Completed"), choices=((False, 'Ongoing'), (True, 'Completed')), default=False)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Proposal Approved")
        verbose_name_plural = _("Proposal Approved")


    def __str__(self):
        return f'{self.team.title} vrs. {self.proposal_sale.proposal.created_by.get_full_name()}'


class ProposalCompletionFiles(models.Model):
    proposal = models.ForeignKey(ProposalResolution, verbose_name=_("Proposal File"), related_name="applicantcompletionfiles", on_delete=models.CASCADE)
    attachment = models.FileField(_("Attachment"), help_text=_("image must be any of these 'jpeg','pdf','jpg','png','psd',"), upload_to=proposal_file_directory, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])])
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Proposal File")
        verbose_name_plural = _("Proposal Files")


    def __str__(self):
        return self.proposal.team.title



class ProposalReview(models.Model):
    resolution = models.ForeignKey(ProposalResolution, verbose_name=_("Proposal Review"), related_name="reviewproposal", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=100)
    message = models.TextField(_("Message"), max_length=650)
    rating = models.PositiveSmallIntegerField(_("Rating"), default=3)
    status = models.BooleanField(_("Confirm Work"), choices=((False, 'Pending'), (True, 'Completed')), default=True)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Proposal Review")
        verbose_name_plural = _("Proposal Review")

    def __str__(self):
        return self.title


    # @classmethod
    # def create(cls, resolution, title, message:str, rating:int):

    #     with db_transaction.atomic(): #nowait=True
    #         if resolution is None:
    #             raise ReviewException(_("Bad request.Please contact Admin"))
    #         if title is None:
    #             raise ReviewException(_("Title is required"))
    #         if message is None:
    #             raise ReviewException(_("message is required"))
    #         if rating is None:
    #             raise ReviewException(_("message is required"))               

    #         review = cls.objects.select_for_update(nowait=True).get(resolution=resolution)

    #         review.save(update_fields=['resolution','title','message','rating'])

    #     return review




