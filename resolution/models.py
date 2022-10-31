from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from account.fund_exception import ReviewException, ContractException
from teams.models import Team
from notification.mailer import application_cancel_email, approve_application_cancel_email
from freelancer.models import FreelancerAccount
from client.models import ClientAccount
from django.utils import timezone
from proposals.utilities import (
    one_day, two_days, three_days, four_days, 
    five_days, six_days, one_week, two_weeks,
    three_weeks, one_month,two_months, three_months, 
    four_months, five_months, six_months
)


def application_file_directory(instance, filename):
    return "application/%s/%s" % (instance.application.team.title, filename)

def proposal_file_directory(instance, filename):
    return "proposal/%s/%s" % (instance.application.team.title, filename)

def contract_file_directory(instance, filename):
    return "proposal/%s/%s" % (instance.contract.team.title, filename)


class OneClickResolution(models.Model):
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
    TWO_MONTH = "two_month"
    THREE_MONTH = "three_months"
    FOUR_MONTH = "four_months"
    FIVE_MONTH = "five_months"
    SIX_MONTH = "six_months"

    ONGOING = 'ongoing'
    DISPUTED = 'disputed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (DISPUTED, _("Disputed")),
        (CANCELLED, _("Cancelled")),
        (COMPLETED, _("Completed")),
    ) 
    # Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='paidoneclickteam', on_delete=models.CASCADE)
    oneclick_sale = models.ForeignKey("transactions.OneClickPurchase", verbose_name=_("One Click Product"), related_name="oneclickaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)   
    status = models.CharField(_("Action Type"), max_length=20, choices=STATUS_CHOICES, default=ONGOING)    
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("One Click Manager")
        verbose_name_plural = _("One Click Manager")

    def __str__(self):
        return f'{self.team.title} vrs. {self.oneclick_sale.client.get_full_name()}'


    @classmethod
    def start_oneclick(cls, oneclick_sale, team):
        with db_transaction.atomic():

            oneclick = cls.objects.create(oneclick_sale=oneclick_sale,team=team,start_time=timezone.now())

            if oneclick.oneclick_sale.category == 'contract':
                if oneclick.oneclick_sale.contract.contract_duration == cls.ONE_DAY:
                    oneclick.end_time = one_day()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.TWO_DAYS:
                    oneclick.end_time =two_days()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.THREE_DAYS:
                    oneclick.end_time = three_days()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.FOUR_DAYS:
                    oneclick.end_time = four_days()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.FIVE_DAYS:
                    oneclick.end_time = five_days()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.SIX_DAYS:
                    oneclick.end_time = six_days()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.ONE_WEEK:
                    oneclick.end_time = one_week()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.TWO_WEEK:
                    oneclick.end_time = two_weeks()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.THREE_WEEK:
                    oneclick.end_time = three_weeks()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.ONE_MONTH:
                    oneclick.end_time = one_month()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.TWO_MONTH:
                    oneclick.end_time = two_months()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.THREE_MONTH:
                    oneclick.end_time = three_months()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.FOUR_MONTH:
                    oneclick.end_time = four_months()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.FIVE_MONTH:
                    oneclick.end_time = five_months()
                    oneclick.save()
                if oneclick.oneclick_sale.contract.contract_duration == cls.SIX_MONTH:
                    oneclick.end_time = six_months()
                    oneclick.save()

            elif oneclick.oneclick_sale.category == 'externalcontract':
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.ONE_DAY:
                    oneclick.end_time = one_day()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.TWO_DAYS:
                    oneclick.end_time =two_days()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.THREE_DAYS:
                    oneclick.end_time = three_days()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.FOUR_DAYS:
                    oneclick.end_time = four_days()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.FIVE_DAYS:
                    oneclick.end_time = five_days()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.SIX_DAYS:
                    oneclick.end_time = six_days()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.ONE_WEEK:
                    oneclick.end_time = one_week()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.TWO_WEEK:
                    oneclick.end_time = two_weeks()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.THREE_WEEK:
                    oneclick.end_time = three_weeks()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.ONE_MONTH:
                    oneclick.end_time = one_month()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.TWO_MONTH:
                    oneclick.end_time = two_months()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.THREE_MONTH:
                    oneclick.end_time = three_months()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.FOUR_MONTH:
                    oneclick.end_time = four_months()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.FIVE_MONTH:
                    oneclick.end_time = five_months()
                    oneclick.save()
                if oneclick.oneclick_sale.extcontract.contract_duration == cls.SIX_MONTH:
                    oneclick.end_time = six_months()
                    oneclick.save()

            elif oneclick.oneclick_sale.category == 'proposal':
                if oneclick.oneclick_sale.proposal.dura_converter == cls.ONE_DAY:
                    oneclick.end_time = one_day()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.TWO_DAYS:
                    oneclick.end_time = two_days()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.THREE_DAYS:
                    oneclick.end_time = three_days()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.FOUR_DAYS:
                    oneclick.end_time = four_days()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.FIVE_DAYS:
                    oneclick.end_time = five_days()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.SIX_DAYS:
                    oneclick.end_time = six_days()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.ONE_WEEK:
                    oneclick.end_time = one_week()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.TWO_WEEK:
                    oneclick.end_time = two_weeks()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.THREE_WEEK:
                    oneclick.end_time = three_weeks()
                    oneclick.save()
                if oneclick.oneclick_sale.proposal.dura_converter == cls.ONE_MONTH:
                    oneclick.end_time = one_month()
                    oneclick.save()

        return oneclick

    @classmethod
    def review_and_approve(cls, resolution_pk, team, title:str, message:str, rating:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution_pk)
            oneclick_team = Team.objects.select_for_update().get(pk=team.id)
            team_manager = FreelancerAccount.objects.select_for_update().get(user=team.created_by)

            if title == '':
                raise ReviewException(_("Title is required"))
            if message == '':
                raise ReviewException(_("Message is required"))
            if rating is None:
                raise ReviewException(_("rating is required"))

            if resolution.status == 'cancelled':
                raise ReviewException(_("Already cancelled and cannot be reviewed"))

            review = OneClickReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.oneclick_sale.salary_paid)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.oneclick_sale.total_earning)
            team_manager.save(update_fields=['available_balance'])

            oneclick_team.team_balance += int(resolution.oneclick_sale.total_earning)
            oneclick_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save()          

            if OneClickCancellation.objects.filter(resolution=resolution, status='initiated').exists():
                OneClickCancellation.objects.get(resolution=resolution, status='initiated').delete()

            return resolution, oneclick_team, team_manager, review

    @classmethod
    def cancel_oneclick(cls, resolution:int, cancel_type:str, message:str):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)

            if resolution.status != 'ongoing':
                raise Exception(_("You cannot cancel at this stage"))

            if resolution.oneclick_sale.category == 'externalcontract':
                raise Exception(_("Bad request. Please check and try again"))

            resolution.status = 'disputed'
            resolution.save()

            message = OneClickCancellation.create(
                resolution=resolution,
                cancel_type=cancel_type,
                message=message
            )
            # db_transaction.on_commit(lambda: application_cancel_email(message))
            print("cancelled requested")
        return resolution, message

    @classmethod
    def approve_and_cancel_oneclick(cls, resolution:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            message = OneClickCancellation.objects.select_for_update().get(resolution=resolution)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=resolution.oneclick_sale.team.created_by)
            client = ClientAccount.objects.select_for_update().get(user=resolution.oneclick_sale.client)            

            if resolution.status != 'disputed':
                raise Exception(_("You cannot approve at this stage"))
            resolution.status = 'cancelled'
            resolution.save()

            if message.status != 'initiated':
                raise Exception(_("You cannot approve at this stage"))
            message.status = 'approved'
            message.save()

            print('Reversal of:', resolution.oneclick_sale.salary_paid)

            freelancer.pending_balance -= int(resolution.oneclick_sale.salary_paid)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(resolution.oneclick_sale.salary_paid)
            client.save(update_fields=['available_balance'])

            # db_transaction.on_commit(lambda: approve_application_cancel_email(resolution))
            print("successfully cancelled")
        return resolution, message, freelancer, client


class OneClickCancellation(models.Model):
    TEAM_EXCEEDED_DEADLINE = 'team_exceeded_deadline'
    TEAM_ABANDONED_WORK = 'team_abandoned_work'
    TEAM_NOT_RESPONDING = 'team_not_responding'
    TEAM_IS_ABUSIVE = 'team_is_abusive'
    ORDERED_WRONG_PRODUCT = 'ordered_wrong_product'
    DIFFERENT_PRODUCT_DELIVERED = 'different_product_delivered'
    CANCELLATION_TYPE = (
        (TEAM_EXCEEDED_DEADLINE, 'Team Exceeded Deadline'),
        (TEAM_ABANDONED_WORK, 'Team Abandoned Work'),
        (TEAM_NOT_RESPONDING, 'Team not Responding to Chat'),
        (TEAM_IS_ABUSIVE, 'Team is Abusive'),
        (ORDERED_WRONG_PRODUCT, 'I Ordered Wrong Product'),
        (DIFFERENT_PRODUCT_DELIVERED, 'A different product delivered')
    )

    INITIATED = 'initiated'
    APPROVED = 'approved'
    STATUS_CHOICES = (
        (INITIATED, 'Initiated'),
        (APPROVED, 'Approved')
    )    
    resolution = models.ForeignKey(OneClickResolution, verbose_name=_("Oneclick"), related_name="canceloneclick", on_delete=models.CASCADE)
    cancel_type = models.CharField(_("Issue Type"), max_length=100, choices=CANCELLATION_TYPE, default=TEAM_EXCEEDED_DEADLINE)
    status = models.CharField(_("Status"), max_length=100, choices=STATUS_CHOICES, default=INITIATED)
    message = models.TextField(_("Additional Message"), max_length=500)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("OneClick Cancelled")
        verbose_name_plural = _("OneClick Cancelled")

    def __str__(self):
        return f'{self.resolution}'

    @classmethod
    def create(cls, resolution, cancel_type, message):
        return cls.objects.create(resolution=resolution,cancel_type=cancel_type,message=message) 


class OneClickReview(models.Model):
    resolution = models.ForeignKey(OneClickResolution, verbose_name=_("OneClick Review"), related_name="reviewoneclick", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=100)
    message = models.TextField(_("Message"), max_length=650)
    rating = models.PositiveSmallIntegerField(_("Rating"), default=3)
    status = models.BooleanField(_("Confirm Work"), choices=((False, 'Pending'), (True, 'Completed')), default=True)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("OneClick Review")
        verbose_name_plural = _("OneClick Review")

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


class ProjectResolution(models.Model):
    '''
    We compare the project completion time and the default values below to obtain end_time
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
    DISPUTED = 'disputed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (DISPUTED, _("Disputed")),
        (CANCELLED, _("Cancelled")),
        (COMPLETED, _("Completed")),
    ) 

    #Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedteam', on_delete=models.CASCADE)
    application = models.ForeignKey("transactions.ApplicationSale", verbose_name=_("Application Accepted"), related_name="projectapplicantsaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default=ONGOING)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Application Manager")
        verbose_name_plural = _("Application Manager")

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

            if resolution.status == 'cancelled':
                raise ReviewException(_("Already cancelled and cannot be reviewed"))

            review = ApplicationReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.application.total_sales_price)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.application.total_earnings)
            team_manager.save(update_fields=['available_balance'])

            applicant_team.team_balance += int(resolution.application.total_earnings)
            applicant_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save()          

            if ApplicationCancellation.objects.filter(resolution=resolution, status='initiated').exists():
                ApplicationCancellation.objects.get(resolution=resolution, status='initiated').delete()

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


    @classmethod
    def cancel_project(cls, resolution:int, cancel_type:str, message:str):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            if resolution.status != 'ongoing':
                raise Exception(_("You cannot cancel at this stage"))
            resolution.status = 'disputed'
            resolution.save()

            message = ApplicationCancellation.create(
                resolution=resolution,
                cancel_type=cancel_type,
                message=message
            )
            db_transaction.on_commit(lambda: application_cancel_email(message))

        return resolution, message


    @classmethod
    def approve_and_cancel_project(cls, resolution:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            message = ApplicationCancellation.objects.select_for_update().get(resolution=resolution)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=resolution.application.team.created_by)
            client = ClientAccount.objects.select_for_update().get(user=resolution.application.purchase.client)            

            if resolution.status != 'disputed':
                raise Exception(_("You cannot approve at this stage"))
            resolution.status = 'cancelled'
            resolution.save()

            if message.status != 'initiated':
                raise Exception(_("You cannot approve at this stage"))
            message.status = 'approved'
            message.save()

            print('Reversal:', resolution.application.total_sales_price)

            freelancer.pending_balance -= int(resolution.application.total_sales_price)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(resolution.application.total_sales_price)
            client.save(update_fields=['available_balance'])

            db_transaction.on_commit(lambda: approve_application_cancel_email(resolution))

        return resolution, message, freelancer, client


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


class ApplicationCancellation(models.Model):
    TEAM_EXCEEDED_DEADLINE = 'team_exceeded_deadline'
    TEAM_ABANDONED_WORK = 'team_abandoned_work'
    TEAM_NOT_RESPONDING = 'team_not_responding'
    TEAM_IS_ABUSIVE = 'team_is_abusive'
    ORDERED_WRONG_PRODUCT = 'ordered_wrong_product'
    DIFFERENT_PRODUCT_DELIVERED = 'different_product_delivered'
    CANCELLATION_TYPE = (
        (TEAM_EXCEEDED_DEADLINE, 'Team Exceeded Deadline'),
        (TEAM_ABANDONED_WORK, 'Team Abandoned Work'),
        (TEAM_NOT_RESPONDING, 'Team not Responding to Chat'),
        (TEAM_IS_ABUSIVE, 'Team is Abusive'),
        (ORDERED_WRONG_PRODUCT, 'I Ordered Wrong Product'),
        (DIFFERENT_PRODUCT_DELIVERED, 'A different product delivered')
    )

    INITIATED = 'initiated'
    APPROVED = 'approved'
    STATUS_CHOICES = (
        (INITIATED, 'Initiated'),
        (APPROVED, 'Approved')
    )    
    resolution = models.ForeignKey(ProjectResolution, verbose_name=_("Application"), related_name="cancelapplication", on_delete=models.CASCADE)
    cancel_type = models.CharField(_("Issue Type"), max_length=100, choices=CANCELLATION_TYPE, default=TEAM_EXCEEDED_DEADLINE)
    status = models.CharField(_("Status"), max_length=100, choices=STATUS_CHOICES, default=INITIATED)
    message = models.TextField(_("Additional Message"), max_length=500)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Application Cancelled")
        verbose_name_plural = _("Application Cancelled")

    def __str__(self):
        return f'{self.resolution}'

    @classmethod
    def create(cls, resolution, cancel_type, message):
        return cls.objects.create(resolution=resolution,cancel_type=cancel_type,message=message) 


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
    DISPUTED = 'disputed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (DISPUTED, _("Disputed")),
        (CANCELLED, _("Cancelled")),
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
        verbose_name = _("Proposal Manager")
        verbose_name_plural = _("Proposal Manager")

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

            if resolution.status == 'cancelled':
                raise ReviewException(_("Already cancelled and cannot be reviewed"))

            review = ProposalReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.proposal_sale.total_sales_price)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.proposal_sale.total_earning)
            team_manager.save(update_fields=['available_balance'])

            proposal_team.team_balance += int(resolution.proposal_sale.total_earning)
            proposal_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save(update_fields=['status'])          

            if ProposalCancellation.objects.filter(resolution=resolution, status='initiated').exists():
                ProposalCancellation.objects.get(resolution=resolution, status='initiated').delete()

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


    @classmethod
    def cancel_proposal(cls, resolution:int, cancel_type:str, message:str):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            if resolution.status != 'ongoing':
                raise Exception(_("You cannot cancel at this stage"))
            resolution.status = 'disputed'
            resolution.save()

            message = ProposalCancellation.create(
                resolution=resolution,
                cancel_type=cancel_type,
                message=message
            )
            # db_transaction.on_commit(lambda: application_cancel_email(message))

        return resolution, message


    @classmethod
    def approve_and_cancel_proposal(cls, resolution:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            message = ProposalCancellation.objects.select_for_update().get(resolution=resolution)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=resolution.proposal_sale.team.created_by)
            client = ClientAccount.objects.select_for_update().get(user=resolution.proposal_sale.purchase.client)            

            if resolution.status != 'disputed':
                raise Exception(_("You cannot approve at this stage"))
            resolution.status = 'cancelled'
            resolution.save()

            if message.status != 'initiated':
                raise Exception(_("You cannot approve at this stage"))
            message.status = 'approved'
            message.save()

            freelancer.pending_balance -= int(resolution.proposal_sale.total_sales_price)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(resolution.proposal_sale.total_sales_price)
            client.save(update_fields=['available_balance'])

            # db_transaction.on_commit(lambda: approve_application_cancel_email(resolution))

        return resolution, message, freelancer, client


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


class ProposalCancellation(models.Model):
    TEAM_EXCEEDED_DEADLINE = 'team_exceeded_deadline'
    TEAM_ABANDONED_WORK = 'team_abandoned_work'
    TEAM_NOT_RESPONDING = 'team_not_responding'
    TEAM_IS_ABUSIVE = 'team_is_abusive'
    ORDERED_WRONG_PRODUCT = 'ordered_wrong_product'
    DIFFERENT_PRODUCT_DELIVERED = 'different_product_delivered'
    CANCELLATION_TYPE = (
        (TEAM_EXCEEDED_DEADLINE, 'Team Exceeded Deadline'),
        (TEAM_ABANDONED_WORK, 'Team Abandoned Work'),
        (TEAM_NOT_RESPONDING, 'Team not Responding to Chat'),
        (TEAM_IS_ABUSIVE, 'Team is Abusive'),
        (ORDERED_WRONG_PRODUCT, 'I Ordered Wrong Product'),
        (DIFFERENT_PRODUCT_DELIVERED, 'A different product delivered')
    )

    INITIATED = 'initiated'
    APPROVED = 'approved'
    STATUS_CHOICES = (
        (INITIATED, 'Initiated'),
        (APPROVED, 'Approved')
    )    
    resolution = models.ForeignKey(ProposalResolution, verbose_name=_("Proposal"), related_name="cancelproposal", on_delete=models.CASCADE)
    cancel_type = models.CharField(_("Issue Type"), max_length=100, choices=CANCELLATION_TYPE, default=TEAM_EXCEEDED_DEADLINE)
    status = models.CharField(_("Status"), max_length=100, choices=STATUS_CHOICES, default=INITIATED)
    message = models.TextField(_("Additional Message"), max_length=500)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Proposal Cancelled")
        verbose_name_plural = _("Proposal Cancelled")

    def __str__(self):
        return f'{self.resolution}'

    @classmethod
    def create(cls, resolution, cancel_type, message):
        return cls.objects.create(resolution=resolution,cancel_type=cancel_type,message=message) 


class ContractResolution(models.Model):
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
    TWO_MONTH = "two_month"
    THREE_MONTH = "three_months"
    FOUR_MONTH = "four_months"
    FIVE_MONTH = "five_months"
    SIX_MONTH = "six_months"

    ONGOING = 'ongoing'
    DISPUTED = 'disputed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (DISPUTED, _("Disputed")),
        (CANCELLED, _("Cancelled")),
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
        verbose_name = _("Contract Manager")
        verbose_name_plural = _("Contract Manager")

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

            if resolution.status == 'cancelled':
                raise ReviewException(_("Already cancelled and cannot be reviewed"))
                
            review = ContractReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.contract_sale.total_sales_price)
            team_manager.save(update_fields=['pending_balance'])

            team_manager.available_balance += int(resolution.contract_sale.total_earning)
            team_manager.save(update_fields=['available_balance'])

            contract_team.team_balance += int(resolution.contract_sale.total_earning)
            contract_team.save(update_fields=['team_balance'])

            resolution.status = 'completed'
            resolution.save(update_fields=['status'])          

            if ContractCancellation.objects.filter(resolution=resolution, status='initiated').exists():
                ContractCancellation.objects.get(resolution=resolution, status='initiated').delete()

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
                contract.end_time = two_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_DAYS:
                contract.end_time = three_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FOUR_DAYS:
                contract.end_time = four_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FIVE_DAYS:
                contract.end_time = five_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.SIX_DAYS:
                contract.end_time = six_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.ONE_WEEK:
                contract.end_time = one_week()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.TWO_WEEK:
                contract.end_time = two_weeks()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_WEEK:
                contract.end_time = three_weeks()
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
                contract.end_time = four_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FIVE_MONTH:
                contract.end_time = five_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.SIX_MONTH:
                contract.end_time = six_months()
                contract.save()

        return contract


    @classmethod
    def cancel_internal_contract(cls, resolution:int, cancel_type:str, message:str):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            if resolution.status != 'ongoing':
                raise Exception(_("You cannot cancel at this stage"))
            resolution.status = 'disputed'
            resolution.save()

            message = ContractCancellation.create(
                resolution=resolution,
                cancel_type=cancel_type,
                message=message
            )
            # db_transaction.on_commit(lambda: application_cancel_email(message))

        return resolution, message


    @classmethod
    def approve_and_cancel_internal_contract(cls, resolution:int):
        with db_transaction.atomic():  
            resolution = cls.objects.select_for_update().get(pk=resolution)
            message = ContractCancellation.objects.select_for_update().get(resolution=resolution)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=resolution.contract_sale.team.created_by)
            client = ClientAccount.objects.select_for_update().get(user=resolution.contract_sale.purchase.client)            

            if resolution.status != 'disputed':
                raise Exception(_("You cannot approve at this stage"))
            resolution.status = 'cancelled'
            resolution.save()

            if message.status != 'initiated':
                raise Exception(_("You cannot approve at this stage"))
            message.status = 'approved'
            message.save()

            freelancer.pending_balance -= int(resolution.contract_sale.total_sales_price)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(resolution.contract_sale.total_sales_price)
            client.save(update_fields=['available_balance'])

            # db_transaction.on_commit(lambda: approve_application_cancel_email(resolution))

        return resolution, message, freelancer, client


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


class ContractCancellation(models.Model):
    TEAM_EXCEEDED_DEADLINE = 'team_exceeded_deadline'
    TEAM_ABANDONED_WORK = 'team_abandoned_work'
    TEAM_NOT_RESPONDING = 'team_not_responding'
    TEAM_IS_ABUSIVE = 'team_is_abusive'
    ORDERED_WRONG_PRODUCT = 'ordered_wrong_product'
    DIFFERENT_PRODUCT_DELIVERED = 'different_product_delivered'
    CANCELLATION_TYPE = (
        (TEAM_EXCEEDED_DEADLINE, 'Team Exceeded Deadline'),
        (TEAM_ABANDONED_WORK, 'Team Abandoned Work'),
        (TEAM_NOT_RESPONDING, 'Team not Responding to Chat'),
        (TEAM_IS_ABUSIVE, 'Team is Abusive'),
        (ORDERED_WRONG_PRODUCT, 'I Ordered Wrong Product'),
        (DIFFERENT_PRODUCT_DELIVERED, 'A different product delivered')
    )

    INITIATED = 'initiated'
    APPROVED = 'approved'
    STATUS_CHOICES = (
        (INITIATED, 'Initiated'),
        (APPROVED, 'Approved')
    )    
    resolution = models.ForeignKey(ContractResolution, verbose_name=_("Contract"), related_name="cancelcontract", on_delete=models.CASCADE)
    cancel_type = models.CharField(_("Issue Type"), max_length=100, choices=CANCELLATION_TYPE, default=TEAM_EXCEEDED_DEADLINE)
    status = models.CharField(_("Status"), max_length=100, choices=STATUS_CHOICES, default=INITIATED)
    message = models.TextField(_("Additional Message"), max_length=500)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Contract Cancelled")
        verbose_name_plural = _("Contract Cancelled")

    def __str__(self):
        return f'{self.resolution}'

    @classmethod
    def create(cls, resolution, cancel_type, message):
        return cls.objects.create(resolution=resolution,cancel_type=cancel_type,message=message) 


class ExtContractResolution(models.Model):
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
    TWO_MONTH = "two_month"
    THREE_MONTH = "three_months"
    FOUR_MONTH = "four_months"
    FIVE_MONTH = "five_months"
    SIX_MONTH = "six_months"

    ONGOING = 'ongoing'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (ONGOING, _("Ongoing")),
        (CANCELLED, _("Cancelled")),
        (COMPLETED, _("Completed")),
    )  
    # Resolution parameters
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='approvedextcontractteam', on_delete=models.CASCADE)
    contract_sale = models.ForeignKey("transactions.ExtContract", verbose_name=_("Contract Awarded"), related_name="extcontractaction", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start Time"), auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time = models.DateTimeField(_("End Time"), auto_now_add=False, auto_now=False, blank=True, null=True)   
    status = models.CharField(_("Action Type"), max_length=20, choices=STATUS_CHOICES, default=ONGOING)    
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
        
    class Meta:
        ordering = ("-created_at",) 
        verbose_name = _("Ext-Contract Manager")
        verbose_name_plural = _("Ext-Contract Manager")

    def __str__(self):
        return f'{self.team.title} vrs. {self.contract_sale.purchase.client.get_full_name()}'


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
            if rating  == '':
                raise ReviewException(_("rating is required"))

            if resolution.status == 'cancelled':
                raise ReviewException(_("Already cancelled and cannot be reviewed"))
                
            review = ExtContractReview.create(
                resolution=resolution, 
                title=title, 
                message=message, 
                rating=rating, 
            )

            team_manager.pending_balance -= int(resolution.contract_sale.total_sales_price)
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
                contract.end_time = two_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_DAYS:
                contract.end_time = three_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FOUR_DAYS:
                contract.end_time = four_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FIVE_DAYS:
                contract.end_time = five_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.SIX_DAYS:
                contract.end_time = six_days()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.ONE_WEEK:
                contract.end_time = one_week()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.TWO_WEEK:
                contract.end_time = two_weeks()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.THREE_WEEK:
                contract.end_time = three_weeks()
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
                contract.end_time = four_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.FIVE_MONTH:
                contract.end_time = five_months()
                contract.save()
            if contract.contract_sale.contract.contract_duration == cls.SIX_MONTH:
                contract.end_time = six_months()
                contract.save()

        return contract


class ExtContractReview(models.Model):
    resolution = models.ForeignKey(ExtContractResolution, verbose_name=_("Contract Review"), related_name="reviewextcontract", on_delete=models.CASCADE)
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

