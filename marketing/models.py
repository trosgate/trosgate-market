from django.db import models, transaction as db_transaction
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from uuid import uuid4
from django.template.defaultfilters import slugify
import secrets
from account.fund_exception import GenException
from client.models import Client
from freelancer.models import Freelancer
from django.core.exceptions import ValidationError
from notification.mailer import new_ticket_email


def ticket_reference_generator():
        generated_reference = secrets.token_urlsafe(12)[:12]
        similar_ref = Ticket.objects.filter(reference=generated_reference)
        while not similar_ref:
            reference = generated_reference
            break
        return reference


class Announcement(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title of the blog must be unique - up to max of 255 words"), unique=True)
    preview = models.TextField(_("Preview"), max_length=350, help_text=_("Preview of the blog must be unique - up to max of 255 words"))
    backlink = models.URLField(_("Target Url"), max_length=2083, null=True, blank=True, help_text=_("If this notice has detail page to read more, this Optional link will be placed after the last word of 'Preview' to send them there"))
    ordering = models.PositiveIntegerField(_("Ordering"), default=1, help_text=_("This determines how each notice will appear to user eg, 1 means topmost position"),)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Publisher"), help_text=_("This blog will be removed if author is deleted"), related_name="announcer", on_delete=models.CASCADE)   

    class Meta:
        ordering=('-created_at',)
        verbose_name = _("Announcement",)
        verbose_name_plural = _("Announcement",)

    def __str__(self):
        return f'{self.title}'


class AutoTyPist(models.Model):
    title = models.CharField(_("Title"), max_length=30, help_text=_("Enter up to 30 Characters long"), blank=True, null=True, unique=True)
    is_active = models.BooleanField(_("Activate"), choices = ((False,'Inactive'), (True, 'Active')), help_text=_("Make active to show on homepage or Inactive to hide from homepage"), default = True)
    ordering = models.PositiveIntegerField(_("Ordering"), default=1, help_text=_("This determines how each text will appear to user eg, 1 means first position"))

    class Meta:
        ordering = ['ordering']
        verbose_name = _("Auto Typist")
        verbose_name_plural = _("Auto Typist")

    def __str__(self):
        return f'{self.title}'


class Blog(models.Model):
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    TYPE = (
        (FREELANCER, _('Freelancer')),
        (CLIENT, _('Client')),
    )
    title = models.CharField(_("Title"), max_length=255, help_text=_("title of the blog must be unique"), unique=True)
    slug = models.SlugField(_("Slug"), max_length=255)
    introduction = models.TextField(_("Introduction"), max_length=300, blank=True, null=True, help_text=_("Optional- Must have a maximum of 350 words"))
    quote = models.CharField(_("Special Quote"), max_length=300, blank=True, null=True, help_text=_("Optional-Must have a maximum of 200 words"))
    type = models.CharField(_("Article Type"), choices=TYPE, default=None, max_length=30) 
    category = models.ForeignKey('general_settings.Category', verbose_name=_("Category"), related_name="blogcategory", on_delete=models.RESTRICT, max_length=250)
    description = RichTextField(verbose_name=_("Details"), max_length=10000, error_messages={"name": {"max_length": _("Description field is required")}},)    
    tags = models.ManyToManyField('general_settings.Skill', verbose_name=_("Blog Tags"), related_name="blogtags")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Likes"), related_name="bloglikes")    
    number_of_likes = models.PositiveIntegerField(_("Total Likes"), default=0)
    identifier = models.CharField(unique=True, blank=True, max_length=100)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    published = models.BooleanField(_("Published"), choices = ((False,'Private'), (True, 'Public')), help_text=_("You can later modify this at your own convenience"), default = True)    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), help_text=_("This blog will be removed if author is deleted"), related_name="blogauthor", on_delete=models.CASCADE)   
    ordering = models.PositiveIntegerField(_("Ordering"), default=1, help_text=_("This determines how each package will appear to user eg, 1 means first position"),)
    thumbnail = models.ImageField(_("Blog Thumbnail"), default='blog/thumbnail.jpg', help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to='blog', blank=True, validators=[FileExtensionValidator(allowed_extensions=['JPG','JPEG','PNG','PSD'])])  

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.identifier == "":
            self.identifier = str(uuid4())
        
        super(Blog, self).save(*args, **kwargs)


class HelpDesk(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    preview = models.TextField(verbose_name=_("Preview"), max_length=1000, default=None, help_text=_("preview max length is 1000"))
    slug = models.SlugField(_("Slug"), max_length=255)
    
    option_one = models.CharField(_("Option #1"), max_length=100, null=True, blank=True)   
    option_one_description = models.TextField(_("Option #1 Description"), max_length=500, null=True, blank=True)   
    option_one_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #1 Description'"))
    option_two = models.CharField(_("Option #2"), max_length=100, null=True, blank=True)   
    option_two_description = models.TextField(_("Option #2 Description"), max_length=500, null=True, blank=True)   
    option_two_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #2 Description'"))
    option_three = models.CharField(_("Option #3"), max_length=100, null=True, blank=True)   
    option_three_description = models.TextField(_("Option #3 Description"), max_length=500, null=True, blank=True)
    option_three_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #3 Description'"))
    option_four = models.CharField(_("Option #4"), max_length=100, null=True, blank=True)   
    option_four_description = models.TextField(_("Option #4 Description"), max_length=500, null=True, blank=True)
    option_four_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #4 Description'"))
    option_five = models.CharField(_("Option #5"), max_length=100, null=True, blank=True)   
    option_five_description = models.TextField(_("Option #5 Description"), max_length=500, null=True, blank=True)
    option_five_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #5 Description'"))
    option_six = models.CharField(_("Option #6"), max_length=100, null=True, blank=True)   
    option_six_description = models.TextField(_("Option #6 Description"), max_length=500, null=True, blank=True)
    option_six_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #6 Description'"))
    option_seven = models.CharField(_("Option #7"), max_length=100, null=True, blank=True)   
    option_seven_description = models.TextField(_("Option #7 Description"), max_length=500, null=True, blank=True)
    option_seven_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #7 Description'"))
    option_eight = models.CharField(_("Option #8"), max_length=100, null=True, blank=True)   
    option_eight_description = models.TextField(_("Option #8 Description"), max_length=500, null=True, blank=True)
    option_eight_backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #8 Description'"))
    option_nine = models.CharField(_("Option #9"), max_length=100, null=True, blank=True)   
    option_nine_description = models.TextField(_("Option #9 Description"), max_length=500, null=True, blank=True)
    option_nine_backlink = models.URLField(_("Back link"), max_length=1500, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Option #9 Description'"))

    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    published = models.BooleanField(_("Make Default"), choices = ((False,'Private'), (True, 'Public')), help_text=_("Only one instance will be shown based on the one that is default"), default = True)    

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.title}'


class Ticket(models.Model):
    # States
    ACTIVE = 'active'
    CLOSED = 'closed'
    REOPEN = 'reopen'
    STATUS = (
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
        (REOPEN, 'Reopen')
    )

    # Product Type
    NOT_APPLICABLE = 'Not Applicable'
    PROPOSAL = 'proposal'
    PROJECT = 'project'
    CONTRACT = 'active'
    PRODUCT_TYPE = (
        (NOT_APPLICABLE, 'Not Applicable'),
        (PROPOSAL, 'Proposal'),
        (PROJECT, 'Project'),
        (CONTRACT, 'Contract')
    )

    # Query Type
    GENERAL_ENQUIRY = 'general_enquiry'
    ACCOUNT_LOGIN_SIGNUP = 'signup_challenge'
    PASSWORD_RESET = 'password_reset'
    TEAM_INVITATION = 'team_invite_issue'
    TEAM_DISPUTE = 'team_dispute'
    QUIZ_QUESTION = 'quiz_q_and_a_issue'
    CHECKOUT_ISSUE = 'checkou_issue'
    ACCOUNT_PAYOUT = 'Account_payout_issues'
    FEES_AND_CHARGES = 'fees_and_charges'
    REVIEW_AND_APPROVAL = 'review_approval_issues'
    ORDER_CANCELLATION = 'order_cancellation_issues'
    PROPOSAL = 'proposal_issue'
    PROJECT = 'project_issue'
    CONTRACT = 'contract_issue'    
    DEPOSIT = 'deposit_challenge'
    WITHDRAWAL = 'withdrawal_challenge'
    CREDIT_PAYMENT = 'credit_payment_challenge'
    TRANSFER = 'transfer_challenge'
    BUG_REPORTING = 'system_bug'
    OTHER_QUERY = 'other_issues'
    QUERY_TYPE = (
        (GENERAL_ENQUIRY, _('1. General Enquiry')),
        (ACCOUNT_LOGIN_SIGNUP, _('2. Signin/Signup Issues')),
        (PASSWORD_RESET, _('3. Password Reset')),
        (TEAM_INVITATION, _('4. Team Invitation Issues')),
        (TEAM_DISPUTE, _('5. Team Members Dispute')),
        (QUIZ_QUESTION, _('6. Quiz, Q&A Issues')),
        (CHECKOUT_ISSUE, _('7. Checkout Challenge')),
        (ACCOUNT_PAYOUT, _('8. Payout Account Issue')),
        (FEES_AND_CHARGES, _('9. Fees and Over-Charges')),
        (REVIEW_AND_APPROVAL, _('10. Order Review/Approval')),
        (ORDER_CANCELLATION, _('11. Order Cancellation')),
        (CREDIT_PAYMENT, _('12. Freelancer Credit')),
        (PROPOSAL, _('13. Proposal Issues')),
        (PROJECT, _('14. Project Issues')),
        (CONTRACT, _('15. Contract Issues')),
        (DEPOSIT, _('16. Deposit Challenge')),
        (WITHDRAWAL, _('17. Withdrawal Challenge')),
        (TRANSFER, _('18. Transfer Challenge')),
        (BUG_REPORTING, _('19. Reporting System Bug')),
        (OTHER_QUERY, _('20. Other Issues'))
    )

    title = models.CharField(_("Title"), max_length=100, help_text=_("title field is Required"))
    slug = models.SlugField(_("Slug"), max_length=100)
    content = models.TextField(_("Message"), max_length=2000)
    reference = models.CharField(_("Ticket #"), unique=True, blank=True, max_length=100)
    states = models.CharField(_("Status"), max_length=20, choices=STATUS, default=ACTIVE)
    query_type = models.CharField(_("Query Type"), max_length=100, choices=QUERY_TYPE, default=GENERAL_ENQUIRY)
    product_type = models.CharField(_("Product Type"), max_length=100, choices=PRODUCT_TYPE, default=NOT_APPLICABLE)
    product_type_reference = models.CharField(_("Product Reference"), max_length=100, null=True, blank=True, help_text=_("Reference for the product type selected"))
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="reporterteam", on_delete=models.SET_NULL, blank=True, null=True, help_text=_("Only Applicable to Freelancer Queries"))
    support = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Current Support"), related_name="firstticketsupport", blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Customer"), related_name="reportersupport", on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Time Created"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Time Modified"), auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'    


    @classmethod
    def create(cls, created_by, title, content, query_type, product_type, team=None, product_type_reference=None):
        with db_transaction.atomic():
            if (product_type == cls.PROPOSAL and product_type_reference == ''):
                raise GenException(_("For product type Proposal, Product reference is required"))
            
            if (product_type == cls.PROJECT and product_type_reference == ''):
                raise GenException(_("For product type Project, Product reference is required"))
            
            if (product_type == cls.CONTRACT and product_type_reference == ''):
                raise GenException(_("For product type Contract, Product reference is required"))
            
            if (query_type == cls.QUERY_TYPE and product_type_reference == ''):
                raise GenException(_("For Query #13, Product reference is required"))
            
            if (query_type == cls.QUERY_TYPE and product_type_reference == ''):
                raise GenException(_("For Query #14, Product reference is required"))
            
            if (query_type == cls.QUERY_TYPE and product_type_reference == ''):
                raise GenException(_("For Query #15, Product reference is required"))

            if Freelancer.objects.filter(user=created_by).exists() and not team:
                raise GenException(_("Error occured with your active team"))

            if title == '':
                raise GenException(_("Title is required"))

            title_count = len(title)
            if len(title) > 100:
                raise GenException(_(f"Ensure content has at most 2000 characters (it has {title_count})"))
            
            if content == '':
                raise GenException(_("Content is required"))

            content_count = len(content)
            if len(content) > 2000:
                raise GenException(_(f"Ensure content has at most 2000 characters (it has {content_count})"))
            
            if query_type == '':
                raise GenException(_("query type is required"))
            
            if Client.objects.filter(user=created_by).exists():
                team = None

            if product_type_reference is None:
                product_type_reference = ''

            try:
                ticket = cls.objects.create(
                    created_by=created_by, 
                    title=title,
                    content=content, 
                    query_type=query_type, 
                    product_type=product_type,
                    product_type_reference=product_type_reference, 
                    team=team, 
                )
                stan = f'{ticket.pk}'.zfill(8)
                ticket.reference = f'TK{ticket.created_by.id}{stan}'
                ticket.slug=slugify(ticket.title) 
                ticket.save()
            except Exception as e:   
                raise GenException(_(f"Sorry! an error occured. Please try again"))

            try:
                new_ticket_email(ticket)
            except Exception as e:
                print('%s' % (str(e)))

        return ticket


class TicketMessage(models.Model):
    content = models.TextField(_("Message"), max_length=2000)
    ticket = models.ForeignKey(Ticket, verbose_name=_("Ticket"), related_name="tickettracker", on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Time Created"), auto_now_add=True)
    support = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Support"), related_name="ticketsupport", blank=True, null=True, on_delete=models.SET_NULL)
    action = models.BooleanField(_("Action"), choices = ((False,'Customer Replied'), (True, 'Admin Replied')), default = True)
    link_title_one = models.CharField(_("Helpful Article Title #1"), max_length=100, null=True, blank=True)   
    link_title_one_backlink = models.URLField(_("Article Title #1 Backlink"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed in the mail to customer'"))
    link_title_two = models.CharField(_("Helpful Article Title #2"), max_length=100, null=True, blank=True)   
    link_title_two_backlink = models.URLField(_("Article Title #2 Backlink"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed in the mail to customer'"))
    
    class Meta:
        ordering = ['created_at']
        verbose_name = ('Ticket Reply')
        verbose_name_plural = ('Ticket Replies')

    def __str__(self):
        return f'{self.ticket.created_by} vs. {self.support}' 

    def clean(self):       
        if  self.link_title_one and not self.link_title_one_backlink:
            raise ValidationError(
                {'link_title_one_backlink': _("'Helpful Article Title #1' and 'Article Title #1 Backlink' must be created together")})
        
        if  self.link_title_one_backlink and not self.link_title_one:
            raise ValidationError(
                {'link_title_one': _("'Helpful Article Title #1' and 'Article Title #1 Backlink' must be created together")})
        
        if  self.link_title_two and not self.link_title_two_backlink:
            raise ValidationError(
                {'link_title_two_backlink': _("'Helpful Article Title #2' and 'Article Title #2 Backlink' must be created together")})
        
        if  self.link_title_two_backlink and not self.link_title_two:
            raise ValidationError(
                {'link_title_two': _("'Helpful Article Title #2' and 'Article Title #2 Backlink' must be created together")})
        
        return super().clean()


    @classmethod
    def create(cls, content, ticket, created_by, supported_by=None): 
        return cls.objects.create(content=content, ticket=ticket, created_by=created_by, supported_by=supported_by)

















