from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from . managers import UserManager
from django.conf import settings
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.urls import reverse
from . utilities import auth_code
from django_cryptography.fields import encrypt
from django.core.exceptions import ValidationError


class Country(models.Model):
    name = models.CharField(_("Country Name"), max_length=100, unique=True)
    country_code = models.CharField(
        _("Country Code"), max_length=10, blank=True)
    flag = models.ImageField(
        _("Country Flag"), upload_to='country_flag/', null=True, blank=True)
    ordering = models.PositiveIntegerField(
        _("Order Priority"), null=True, blank=True)
    supported = models.BooleanField(_("Supported"), choices=(
        (False, 'No'), (True, 'Yes')), default=True)
    official_name = models.CharField(
        _("Official Name"), max_length=100, blank=True)

    class Meta:
        ordering = ["ordering"]
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

    def flag_tag(self):
        if self.flag:
            return mark_safe('<img src="/media/%s" width="20" height="20" />' % (self.flag))
        else:
            return self.country_code

    flag_tag.short_description = 'flag'


class State(models.Model):
    name = models.CharField(_("State/City"), max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name=_(
        "Country"), null=True, blank=True, related_name='states', on_delete=models.CASCADE)

    class Meta:
        ordering = ["country"]
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name


class Customer(AbstractBaseUser, PermissionsMixin):

    ADMIN = 'admin'
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    USER_TYPE = (
        (ADMIN, _('Admin')),
        (FREELANCER, _('Freelancer')),
        (CLIENT, _('Client')),
    )
    email = models.EmailField(_("Email Address"), max_length=100, unique=True)
    short_name = models.CharField(_("Username"), max_length=30, unique=True)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last Login"), auto_now=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, 
        verbose_name=_("Country"), 
        null=True, blank=True, 
        related_name="countries", 
        on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(_("Activate User"), default=False, help_text="Important: This controls login access for Staffs, Freelancer and CLient")
    is_staff = models.BooleanField(_("Activate Staff"), default=False, help_text="Important: Addition to 'Activate/Deactivate User Login', this controls login access for SuperAdmin and Staffs only")
    is_superuser = models.BooleanField(_("CEO/SuperAdmin"), default=False)
    is_assistant = models.BooleanField(_("Virtual Assistant"), default=False)
    user_type = models.CharField(_("User Type"), choices=USER_TYPE, max_length=30)
    
    class Meta:
        ordering = ("-date_joined",)
        verbose_name = "User Manager"
        verbose_name_plural = "User Manager"

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['short_name', 'user_type']
    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.short_name

    def get_username(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def clean(self):
        if self.is_superuser == True and self.is_staff == False:
            raise ValidationError(
                {'is_staff': _('Superuser must have "Activate Staff" set to Active')})
        
        if self.is_assistant == True and self.is_staff == False:
            raise ValidationError(
                {'is_staff': _('Assistant must have "Activate Staff" set to Active')})
        
        if Customer.objects.filter(is_superuser=True).count() > 1 and self.is_superuser == True:
            raise ValidationError(
                {'is_superuser': _('SuperAdmin role is too strong to share. Maybe add them as Virtual Assistants or exchange credentials at your own risk')})

        if self.user_type == 'freelancer' and self.is_assistant == True:
            raise ValidationError(
                {'is_assistant': _('Freelancer cannot be a Staff or Assistant at same time. You can let them join with a different email')})
        
        if self.user_type == 'client' and self.is_assistant == True:
            raise ValidationError(
                {'is_assistant': _('Client cannot be a Staff or Assistant at same time. You can let them join with a different email')})
           
        return super().clean()


class TwoFactorAuth(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='twofactorauth', on_delete=models.CASCADE)
    pass_code = encrypt(models.CharField(max_length=255, blank=True, null=True))
    last_login = models.DateTimeField(_("Last Login"), auto_now=True)
    
    def __str__(self):
        return f'{self.user.get_full_name()}'    

    def save(self, *args, **kwargs):
        self.pass_code = auth_code()
        super(TwoFactorAuth, self).save(*args, **kwargs)
































