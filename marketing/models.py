from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from uuid import uuid4
from django.template.defaultfilters import slugify
import secrets


def ticket_reference_generator():
        generated_reference = secrets.token_urlsafe(12)[:12]
        similar_ref = Ticket.objects.filter(reference=generated_reference)
        while not similar_ref:
            reference = generated_reference
            break
        return reference


class Announcement(models.Model):
    content = models.CharField(_("Content"), max_length=255, help_text=_("title of the blog must be unique"), unique=True)
    backlink = models.URLField(_("Target Url"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'Content'"))
    default = models.BooleanField(_("Default"), choices = ((False,'Private'), (True, 'Public')), default = False)
    
    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcement")

    def __str__(self):
        return f'{self.content}'


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
    type = models.CharField(_("Article Type"), choices=TYPE, default=None, max_length=30) 
    category = models.ForeignKey('general_settings.Category', verbose_name=_("Category"), related_name="blogcategory", on_delete=models.RESTRICT, max_length=250)
    description = RichTextField(verbose_name=_("Description"), max_length=20000, error_messages={"name": {"max_length": _("Description field is required")}},)    
    tags = models.ManyToManyField('general_settings.Skill', verbose_name=_("Blog Tags"), related_name="blogtags")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Likes"), related_name="bloglikes")    
    number_of_likes = models.PositiveIntegerField(_("Total Likes"), default=0)
    identifier = models.CharField(unique=True, blank=True, max_length=100)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    published = models.BooleanField(_("Published"), choices = ((False,'Private'), (True, 'Public')), help_text=_("You can later modify this at your own convenience"), default = True)    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), help_text=_("This blog will be removed if author is deleted"), related_name="blogauthor", on_delete=models.CASCADE)   
    ordering = models.PositiveIntegerField(_("Ordering"), default=1, help_text=_("This determines how each package will appear to user eg, 1 means first position"), validators=[MinValueValidator(1), MaxValueValidator(3)])
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


class Ticket(models.Model):
    OPEN = 'open'
    REVIEW = 'review'
    CLOSED = 'closed'
    STATES = (
        (OPEN, 'Open'),
        (REVIEW, 'Review'),
        (CLOSED, 'Closed')
    )

    # Package status
    PROPOSAL = 'proposal'
    PROJECT = 'project'
    CONTRACT = 'active'
    QUERY_TYPE = (
        (PROPOSAL, 'Proposal'),
        (PROJECT, 'Project'),
        (CONTRACT, 'Contract')
    )    
    title = models.CharField(_("Title"), max_length=150, help_text=_("title field is Required"))
    content = models.TextField(_("Message"), max_length=500)
    reference = models.CharField(unique=True, blank=True, max_length=100)
    query_type = models.CharField(_("Query Type"), max_length=20, choices=QUERY_TYPE, default=None)
    query_type_reference = models.CharField(_("Query Reference"), max_length=20, help_text=_("Reference for the Query type selected"))
    states = models.CharField(_("Query Type"), max_length=20, choices=STATES, default=OPEN)
    
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="reporterteam", on_delete=models.SET_NULL, blank=True, null=True, help_text=_("Only Applicable to Freelancer Queries"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Reporter"), related_name="reportersupport", on_delete=models.CASCADE)
    assisted_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Support Team"), related_name="adminsupport", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.reference == "":
            self.reference = ticket_reference_generator()
        super(Ticket, self).save(*args, **kwargs)

    




































