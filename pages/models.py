from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe


class TermsAndConditions(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    description = RichTextField(verbose_name=_("Description"), max_length=3500, help_text=_("Description max length is 3500"))
    is_published = models.BooleanField(_("Show/Hide"), choices = ((False,'Private'), (True, 'Public')), default = False)
    slug = models.SlugField(_("Slug"), max_length=255)
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    ordering = models.PositiveIntegerField(_("Order Priority"), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('ordering',)
        verbose_name = _("T & C")
        verbose_name_plural = _("T & C")


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
    ordering = models.PositiveIntegerField(_("Order Priority"), null=True, blank=True)

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


class Sponsorship(models.Model):
    title = models.CharField(_("Title"), max_length=255, help_text=_("title field is Required"), unique=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, help_text=_("subtitle field is optional with length of 200 characters"), blank=True, null=True)
    preview = models.TextField(verbose_name=_("Preview"), max_length=1000, default=None, help_text=_("preview max length is 1000"))
    is_published = models.BooleanField(_("Show/Hide"), choices = ((False,'Private'), (True, 'Public')), default = False)
    slug = models.SlugField(_("Slug"), max_length=255)
    thumbnail = models.ImageField(_("Proposal Thumbnail"), default='default-thumbnail.jpg', help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to="howitworks/thumbnail", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['JPG','JPEG','PNG','PSD'])])  
    backlink = models.URLField(_("Back link"), max_length=2083, null=True, blank=True, help_text=_("This Optional link will be placed after the last word of 'preview'"))

    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("How it Works - Sponsorship")
        verbose_name_plural = _("How it Works - Sponsorship")

    def get_sponsorship_tag(self):
        if self.thumbnail:
            return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.thumbnail))
        else:
            return f'/static/images/default-thumbnail.jpg'

    get_sponsorship_tag.short_description = 'thumbnail'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Sponsorship, self).save(*args, **kwargs)


class Sponsor(models.Model):
    name = models.CharField(_("Full Name"), max_length=100, help_text=_("Title field is Required"))
    email = models.EmailField(_("Email"), max_length=100, help_text=_("Email field is Required"), unique=True)
    availability1 = models.DateTimeField(_("Availability One"), auto_now_add=False, help_text=_("Times we can call you"), blank=True, null=True)
    availability2 = models.DateTimeField(_("Availability Two"), auto_now_add=False, help_text=_("Times to call you"), blank=True, null=True)
    availability3 = models.DateTimeField(_("Availability Three"), auto_now_add=False, help_text=_("Times to call you"), blank=True, null=True)
    comment = models.TextField(verbose_name=_("Comment"), max_length=500, blank=True, null=True, help_text=_("Any comment you have"))
    created_at = models.DateTimeField(_("Created On"), auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")




























