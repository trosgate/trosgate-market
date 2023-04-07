from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django_cryptography.fields import encrypt
from account.utilities import auth_code as get_token
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


def aboutus_path(instance, filename):
    return "aboutus/%s/%s" % (instance.title, filename)


class TermsAndConditions(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    quote = models.TextField(_("Quote"), max_length=350, help_text=_("This optional text will appear at the top of Description"), blank=True, null=True)
    description = RichTextField(verbose_name=_("Description"), max_length=3500, help_text=_("Description max length is 3500"))
    is_published = models.BooleanField(_("Show/Hide"), choices = ((False,'Private'), (True, 'Public')), default = False)
    slug = models.SlugField(_("Slug"), max_length=255)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    ordering = models.PositiveIntegerField(_("Order Priority"), null=True, blank=True)
    objects = models.Manager()
    sites = models.ManyToManyField(Site)
    tenants = CurrentSiteManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('ordering',)
        verbose_name = _("Terms of Service")
        verbose_name_plural = _("Terms of Service")


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(TermsAndConditions, self).save(*args, **kwargs)


class Hiring(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, help_text=_("subtitle field is optional with length of 200 characters"), blank=True, null=True)
    preview = models.TextField(verbose_name=_("Preview"), max_length=1000, default=None, help_text=_("preview max length is 1000"))
    is_published = models.BooleanField(_("Show/Hide"), choices = ((False,'Private'), (True, 'Public')), default = False)
    slug = models.SlugField(_("Slug"), max_length=255)
    thumbnail = models.ImageField(_("Proposal Thumbnail"), default='default-thumbnail.jpg', help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to="howitworks/thumbnail", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG','JPEG','PNG','PSD'])])  
    backlink = models.URLField(_("Back link"), max_length=1000, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'preview'"))

    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    ordering = models.PositiveIntegerField(_("Order Priority"), default=0)

    def get_howitwork_hiring_tag(self):
        if self.thumbnail:
            return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (self.thumbnail))
        else:
            return f'/static/images/default-thumbnail.png'

    get_howitwork_hiring_tag.short_description = 'thumbnail'

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('ordering',)
        verbose_name = _("How it Works - Hiring")
        verbose_name_plural = _("How it Works - Hiring")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Hiring, self).save(*args, **kwargs)


class Freelancing(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, help_text=_("subtitle field is optional with length of 200 characters"), blank=True, null=True)
    preview = models.TextField(verbose_name=_("Preview"), max_length=1000, default=None, help_text=_("preview max length is 1000"))
    is_published = models.BooleanField(_("Show/Hide"), choices = ((False,'Private'), (True, 'Public')), default = False)
    slug = models.SlugField(_("Slug"), max_length=255)
    thumbnail = models.ImageField(_("Proposal Thumbnail"), default='default-thumbnail.jpg', help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to="howitworks/thumbnail", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG','JPEG','PNG','PSD'])])  
    backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'preview'"))
    
    option_one = models.CharField(_("Option #1"), max_length=100, null=True, blank=True)   
    option_one_description = models.TextField(_("Option #1 Description"), max_length=500, null=True, blank=True)   
    option_two = models.CharField(_("Option #2"), max_length=100, null=True, blank=True)   
    option_two_description = models.TextField(_("Option #2 Description"), max_length=500, null=True, blank=True)   
    option_three = models.CharField(_("Option #3"), max_length=100, null=True, blank=True)   
    option_three_description = models.TextField(_("Option #3 Description"), max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("How it Works - Freelancing")
        verbose_name_plural = _("How it Works - Freelancing")

    def get_howitwork_freelancing_tag(self):
        if self.thumbnail:
            return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.thumbnail))
        else:
            return f'/static/images/default-thumbnail.jpg'

    get_howitwork_freelancing_tag.short_description = 'thumbnail'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Freelancing, self).save(*args, **kwargs)


class AboutUsPage(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, help_text=_("subtitle field is optional with length of 200 characters"), blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"), max_length=3500, default="This is the description of the about page This is the description of the about page This is the description of the about page This is the description of the about page", help_text=_("Description max length is 3500"))
    display_stats = models.BooleanField(_("Display Stats"), choices=((True, 'Yes'), (False, 'No')), default=True)
    banner_type = models.BooleanField(_("Media Switch"), choices=((True, 'Activate Video'), (False, 'Activate Banner')), default=False)
    ad_image = models.ImageField(_("Ad Image"), help_text=_("image must be any of these: 'JPEG','JPG','PNG','PSD'"), null=True, blank=True, upload_to=aboutus_path, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    slug = models.SlugField(_("Slug"), max_length=255)
    title_block = models.CharField(_("Banner Title"), max_length=100, default="Hire Experts or Team")
    subtitle_block = models.CharField(_("Banner Subtitle"), max_length=150, default="Consectetur adipisicing elit sed dotem eiusmod tempor incuntes ut labore etdolore maigna aliqua enim.")
    banner_color = models.CharField(_("Banner Background Color"), max_length=100, default="purple", help_text=_("Put your color here to decorate Banner Background and buttons like signup and login. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes"), null=True, blank=True)
    banner_button_one_color = models.CharField(_("Banner Button1 Color"), max_length=100, default="green", help_text=_("Put your bootstrap color here to decorate Banner Button 1. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes"), null=True, blank=True)
    banner_button_two_color = models.CharField(_("Banner Button2 Color"), max_length=100, default="light", help_text=_("Put your bootstrap color here to decorate Banner Button 2. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes"), null=True, blank=True)
    banner_image = models.ImageField(_("Hero Image"), help_text=_("image must be any of these: 'JPEG','JPG','PNG','PSD'"), null=True, blank=True, upload_to=aboutus_path, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    video_url= models.URLField(
        _("Embed Video Url"), 
        max_length=2083, 
        null=True, 
        blank=True, 
        help_text=_("Enter the full path to your video url on youtube or vimeo etc")
    )
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("About Us Page")
        verbose_name_plural = _("About Us Page")


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(AboutUsPage, self).save(*args, **kwargs)

    def clean(self):
        if self.banner_type == True and not self.video_url:
            raise ValidationError(
                {"video_url": _("If Media switch is Video, then 'Embed Video' option must be provided.")})
        if self.banner_type == False and not self.ad_image:
            raise ValidationError(
                {"ad_image": _("If Media switch is Banner, then 'About Banner' option must be provided.")})


class Investor(models.Model):
    MR = 'mr'
    MRS = 'mrs'
    SIR = 'sir'
    MISS = 'miss'
    DR = 'dr'
    PROF = 'prof'
    HON = 'hon'
    SALUTAION_CHOICES = (
        (MR, _('Mr.')),
        (MRS, _('Mrs.')),
        (SIR, _('Sir')),
        (MISS, _('Miss')),
        (HON, _('Hon')),
        (DR, _('Dr.')),
        (PROF, _('Prof')),
    )        
    salutation = models.CharField(_("Title"), max_length=10, choices=SALUTAION_CHOICES, default=MR, help_text=_("How would you like us to address you?"))
    verified = models.BooleanField(_("Verified"), default=False)
    myname = models.CharField(_("Full Name"), max_length=100)
    myemail = models.EmailField(_("Email"), max_length=100)
    myconfirm_email = models.EmailField(_("Confirm Email"), max_length=100)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return f"{self.get_salutation_display()} {self.myname}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Investors")
        verbose_name_plural = _("Investors")


    @classmethod
    def check_or_create(cls, salutation, myname, myemail, myconfirm_email):
        with db_transaction.atomic():
            if Investor.objects.filter(myemail=myemail).exists():
                 raise Exception(_("Your record is already verified. We will keep touch if we havent yet"))
            
            if myemail != myconfirm_email:
                raise Exception("Emails donnot match. Try again")

            investor = cls.objects.create(
                salutation=salutation, 
                myname=myname, 
                myemail=myemail, 
                myconfirm_email=myconfirm_email,
                verified = True
            )
        return investor





















