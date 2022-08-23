from email.mime import application
from turtle import title
from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from account.fund_exception import ReviewException
from teams.models import Team
from freelancer.models import FreelancerAccount
from django.utils import timezone
from proposals.utilities import (
    one_day, two_days, three_days, four_days, 
    five_days, six_days, one_week, two_weeks,
    three_weeks, one_month,
    #Below additional times apply to contract
    two_months, three_months, four_months, five_months, six_months
)


def application_file_directory(instance, filename):
    return "application/%s/%s" % (instance.application.team.title, filename)

def proposal_file_directory(instance, filename):
    return "proposal/%s/%s" % (instance.application.team.title, filename)

def contract_file_directory(instance, filename):
    return "proposal/%s/%s" % (instance.contract.team.title, filename)


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

    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (COMPLETED, _("Completed")),
    ) 

    #Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedteam', on_delete=models.CASCADE)
    application = models.ForeignKey("transactions.ApplicationSale", verbose_name=_("Application Accepted"), related_name="projectapplicantsaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    status = models.CharField(_("Action Type"), max_length=20, choices=STATUS_CHOICES, default=ONGOING)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Application Approved")
        verbose_name_plural = _("Application Approved")

    def __str__(self):
        return f'{self.team.title}'


    @classmethod
    def review_and_approve(cls, resolution_pk, team, title:str, message:str, rating:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution_pk)
            applicant_team = Team.objects.select_for_update().get(pk=team.id)
            team_manager = FreelancerAccount.objects.select_for_update().get(user=team.created_by)

            if title == '':
                raise ReviewException(_("Title is required"))
            if message == '':
                raise ReviewException(_("Message is required"))
            if rating is None:
                raise ReviewException(_("rating is required"))

            review = ApplicationReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.application.total_earnings)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.application.total_earnings)
            team_manager.save(update_fields=['available_balance'])

            applicant_team.team_balance += int(resolution.application.total_earnings)
            applicant_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save(update_fields=['status'])          

            return resolution, applicant_team, team_manager, review


    @classmethod
    def start_new_project(cls, application, team):
        with db_transaction.atomic():  

            project = cls.objects.create(
                application=application, team=team, start_time=timezone.now()
            )

            if project.application.project.completion_time == cls.ONE_DAY:
                project.end_time = one_day()
                project.save()
            if project.application.project.completion_time == cls.TWO_DAYS:
                project.end_time =two_days()
                project.save()
            if project.application.project.completion_time == cls.THREE_DAYS:
                project.end_time = three_days()
                project.save()
            if project.application.project.completion_time == cls.FOUR_DAYS:
                project.end_time = four_days()
                project.save()
            if project.application.project.completion_time == cls.FIVE_DAYS:
                project.end_time = five_days()
                project.save()
            if project.application.project.completion_time == cls.SIX_DAYS:
                project.end_time = six_days()
                project.save()
            if project.application.project.completion_time == cls.ONE_WEEK:
                project.end_time = one_week()
                project.save()
            if project.application.project.completion_time == cls.TWO_WEEK:
                project.end_time = two_weeks()
                project.save()
            if project.application.project.completion_time == cls.THREE_WEEK:
                project.end_time = three_weeks()
                project.save()
            if project.application.project.completion_time == cls.ONE_MONTH:
                project.end_time = one_month()
                project.save()

        return project


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
        verbose_name = _("Application Review")
        verbose_name_plural = _("Application Review")

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, resolution, title, message, rating):
        
        if title is None:
            raise ReviewException(_("Title is required"))
        if message is None:
            raise ReviewException(_("Message is required"))
        if rating is None:
            raise ReviewException(_("rating is required"))   

        return cls.objects.create(resolution=resolution, title=title, message=message, rating=rating, status = True)



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

    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (COMPLETED, _("Completed")),
    ) 
    #Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedproposalteam', on_delete=models.CASCADE)
    proposal_sale = models.ForeignKey("transactions.ProposalSale", verbose_name=_("Proposal Sold"), related_name="proposalaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)   
    status = models.CharField(_("Action Type"), max_length=20, choices=STATUS_CHOICES, default=ONGOING)    
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Proposal Approved")
        verbose_name_plural = _("Proposal Approved")

    def __str__(self):
        return f'{self.team.title} vrs. {self.proposal_sale.proposal.created_by.get_full_name()}'


    @classmethod
    def review_and_approve(cls, resolution_pk, team, title:str, message:str, rating:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution_pk)
            proposal_team = Team.objects.select_for_update().get(pk=team.id)
            team_manager = FreelancerAccount.objects.select_for_update().get(user=team.created_by)

            if title is None:
                raise ReviewException(_("Title is required"))
            if message is None:
                raise ReviewException(_("Message is required"))
            if rating is None:
                raise ReviewException(_("rating is required"))

            review = ProposalReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.proposal_sale.total_earning)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.proposal_sale.total_earning)
            team_manager.save(update_fields=['available_balance'])

            proposal_team.team_balance += int(resolution.proposal_sale.total_earning)
            proposal_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save(update_fields=['status'])          

            return resolution, proposal_team, team_manager, review


    @classmethod
    def start_new_proposal(cls, proposal_sale, team):
        with db_transaction.atomic():  

            proposal = cls.objects.create(
                proposal_sale=proposal_sale, team=team, start_time=timezone.now()
            )

            if proposal.proposal_sale.proposal.dura_converter == cls.ONE_DAY:
                proposal.end_time = one_day()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.TWO_DAYS:
                proposal.end_time = two_days()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.THREE_DAYS:
                proposal.end_time = three_days()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.FOUR_DAYS:
                proposal.end_time = four_days()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.FIVE_DAYS:
                proposal.end_time = five_days()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.SIX_DAYS:
                proposal.end_time = six_days()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.ONE_WEEK:
                proposal.end_time = one_week()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.TWO_WEEK:
                proposal.end_time = two_weeks()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.THREE_WEEK:
                proposal.end_time = three_weeks()
                proposal.save()
            if proposal.proposal_sale.proposal.dura_converter == cls.ONE_MONTH:
                proposal.end_time = one_month()
                proposal.save()

        return proposal


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

    @classmethod
    def create(cls, resolution, title, message, rating):
        
        if title is None:
            raise ReviewException(_("Title is required"))
        if message is None:
            raise ReviewException(_("Message is required"))
        if rating is None:
            raise ReviewException(_("rating is required"))   

        return cls.objects.create(resolution=resolution, title=title, message=message, rating=rating, status = True)


class ContractResolution(models.Model):
    '''
    We used signal to compare the contract completion time and the default values below to obtain end_time
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

    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (COMPLETED, _("Completed")),
    ) 
    # Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedcontractteam', on_delete=models.CASCADE)
    contract_sale = models.ForeignKey("transactions.ContractSale", verbose_name=_("Contract Awarded"), related_name="contractaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)   
    status = models.CharField(_("Action Type"), max_length=20, choices=STATUS_CHOICES, default=ONGOING)    
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Contract Awarded")
        verbose_name_plural = _("Contract Awarded")

    def __str__(self):
        return f'{self.team.title} vrs. {self.contract_sale.contract.created_by.get_full_name()}'


    @classmethod
    def review_and_approve(cls, resolution_pk, team, title:str, message:str, rating:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution_pk)
            contract_team = Team.objects.select_for_update().get(pk=team.id)
            team_manager = FreelancerAccount.objects.select_for_update().get(user=team.created_by)

            if title == '':
                raise ReviewException(_("Title is required"))
            if message == '':
                raise ReviewException(_("Message is required"))
            if rating is None:
                raise ReviewException(_("rating is required"))

            review = ContractReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.contract_sale.total_earning)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.contract_sale.total_earning)
            team_manager.save(update_fields=['available_balance'])

            contract_team.team_balance += int(resolution.contract_sale.total_earning)
            contract_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save(update_fields=['status'])          

            return resolution, contract_team, team_manager, review


    @classmethod
    def start_new_contract(cls, contract_sale, team):
        with db_transaction.atomic():  

            contract = cls.objects.create(
                contract_sale=contract_sale, team=team, start_time=timezone.now()
            )

            if contract.contract_sale.contract.contract_duration == cls.ONE_DAY:
                contract.end_time = one_day()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.TWO_DAYS:
                contract.end_time =two_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_DAYS:
                contract.end_time =three_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FOUR_DAYS:
                contract.end_time =four_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FIVE_DAYS:
                contract.end_time =five_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.SIX_DAYS:
                contract.end_time =six_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.ONE_WEEK:
                contract.end_time =one_week()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.TWO_WEEK:
                contract.end_time =two_weeks()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_WEEK:
                contract.end_time =three_weeks()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.ONE_MONTH:
                contract.end_time =one_month()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.TWO_MONTH:
                contract.end_time =two_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_MONTH:
                contract.end_time =three_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FOUR_MONTH:
                contract.end_time =four_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FIVE_MONTH:
                contract.end_time =five_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.SIX_MONTH:
                contract.end_time =six_months()
                contract.save()

        return contract


class ContractReview(models.Model):
    resolution = models.ForeignKey(ContractResolution, verbose_name=_("Contract Review"), related_name="reviewcontract", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=100)
    message = models.TextField(_("Message"), max_length=650)
    rating = models.PositiveSmallIntegerField(_("Rating"), default=3)
    status = models.BooleanField(_("Confirm Work"), choices=((False, 'Pending'), (True, 'Completed')), default=True)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Contract Review")
        verbose_name_plural = _("Contract Review")

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, resolution, title, message, rating):
        
        if title == '':
            raise ReviewException(_("Title is required"))
        if message == '':
            raise ReviewException(_("Message is required"))
        if rating is None:
            raise ReviewException(_("rating is required"))   

        return cls.objects.create(resolution=resolution, title=title, message=message, rating=rating, status = True)


class ContractCompletionFiles(models.Model):
    contract = models.ForeignKey(ContractResolution, verbose_name=_("Contract File"), related_name="contractcompletionfiles", on_delete=models.CASCADE)
    attachment = models.FileField(_("Attachment"), help_text=_("image must be any of these 'jpeg','pdf','jpg','png','psd',"), upload_to=contract_file_directory, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])])
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Contract File")
        verbose_name_plural = _("Contract Files")


    def __str__(self):
        return self.contract.team.title


