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
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from .import constant
import datetime
from general_settings.models import SettingsMaster



class Country(models.Model):
    name = models.CharField(_("Country Name"), max_length=255, unique=True)
    country_code = models.CharField(_("Country Code"), max_length=150, blank=True)
    region = models.CharField(_("Continent"), max_length=255, null=True, blank=True)
    subregion = models.CharField(_("Sub Continent"), max_length=255, null=True, blank=True)
    latitude = models.CharField(_("Latitude"), max_length=255, null=True, blank=True)
    longitude = models.CharField(_("Longitude"), max_length=255, null=True, blank=True)
    currency_name = models.CharField(_("Currency"), max_length=255, null=True, blank=True)
    currency = models.CharField(_("Currency"), max_length=255, blank=True)
    phone_code = models.CharField(_("Phone Code"), max_length=255, blank=True)
    
    flag = models.ImageField(
        _("Country Flag"), upload_to='country_flag/', null=True, blank=True)
    ordering = models.PositiveIntegerField(
        _("Order Priority"), null=True, blank=True)
    supported = models.BooleanField(_("Supported"), choices=(
        (False, 'No'), (True, 'Yes')), default=True)
    
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
    name = models.CharField(_("State Name"), max_length=255, blank=True)
    state_code = models.CharField(_("State Code"), max_length=100, blank=True)
    latitude = models.CharField(_("latitude"), max_length=255, blank=True, null=True)
    longitude = models.CharField(_("longitude"), max_length=255,blank=True, null=True)
    country = models.ForeignKey(Country, 
        verbose_name=_("Country"), 
        related_name="states", 
        on_delete=models.CASCADE
    )
    ordering = models.PositiveIntegerField(
        _("Order Priority"), null=True, blank=True)
    
    class Meta:
        ordering = ["ordering"]
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(_("City Name"), max_length=255, blank=True)
    latitude = models.CharField(_("latitude"), max_length=255, blank=True, null=True)
    longitude = models.CharField(_("longitude"), max_length=255,blank=True, null=True)
    wikidata = models.CharField(_("Wiki Data Id"), max_length=255,blank=True, null=True)
    country = models.ForeignKey(Country, 
        verbose_name=_("Country"), 
        related_name="cities", 
        on_delete=models.CASCADE
    )
    state = models.ForeignKey(State, verbose_name=_("State"), related_name="cities", on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField(
        _("Order Priority"), null=True, blank=True)
    
    class Meta:
        ordering = ["ordering"]
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.name


class Customer(AbstractBaseUser, PermissionsMixin):

    ADMIN = 'admin'
    MERCHANT = 'merchant'
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    USER_TYPE = (
        (ADMIN, _('Admin')),
        (MERCHANT, _('Merchant')),
        (FREELANCER, _('Freelancer')),
        (CLIENT, _('Client')),
    )
    email = models.EmailField(_("Email Address"), max_length=100, unique=True)
    short_name = models.CharField(_("Username"), max_length=30, blank=True, null=True, unique=True)
    first_name = models.CharField(_("First Name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=50, blank=True, null=True)
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
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    active_merchant_id = models.PositiveIntegerField(_("Active Merchant ID"), default=0)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last Login"), auto_now=True)

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = "User Manager"
        verbose_name_plural = "User Manager"

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.short_name if self.short_name else self.first_name

    def get_username(self):
        return self.email
    
    @property
    def is_freelancer(self):
        return self.user_type == 'freelancer' and self.is_active == True
    
    @property
    def is_client(self):
        return self.user_type == 'client' and self.is_active == True
    
    @property
    def is_merchant(self):
        return self.user_type == 'merchant' and self.is_active == True
    
    @property
    def is_admin(self):
        return self.user_type == 'admin' and self.is_active == True and self.is_staff == True

    def email_user(self, subject, message, from_email, **kwargs):
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
                {'is_staff': _('Virtual Assistant cannot be active when "Activate Staff" status is disabled')})
        
        if self.user_type == 'freelancer' and self.is_assistant == True:
            raise ValidationError(
                {'is_assistant': _('Freelancer cannot be a Staff or Assistant at same time. You can let them join with a different email and username')})
        
        if self.user_type == 'client' and self.is_assistant == True:
            raise ValidationError(
                {'is_assistant': _('Client cannot be a Staff or Assistant at same time. You can let them join with a different email and username')})
           
        return super().clean()


class Package(models.Model):
    #
    # Package Type
    STARTER = 'Basic'
    STANDARD = 'Team'
    LATEST = 'Enterprise'
    STATUS = (
        (STARTER, _('Starter')),
        (STANDARD, _('Standard')),
        (LATEST, _('Enterprise')),
    )

    #
    # Initial Plan Configuration
    type = models.CharField(_("Package Type"), choices=STATUS, default=STARTER, unique=True, max_length=50)
    verbose_type = models.CharField(_("Branded Name"), unique=True, blank=True, null=True, help_text=_("Customize name for the package. If empty, the default names will be displayed"), max_length=50)
    can_change_domain = models.BooleanField(_("Domain Change"), choices=((False, 'No'), (True, 'Yes')), default=False, help_text=_("Merchant with this package can change domain"),)
    ssl_activation = models.BooleanField(_("SSL Installation"), choices=((False, 'No'), (True, 'Yes')), default=True, help_text=_("Domains on site will be provided with ssl. We recommend actiovation for all domains"),)
    max_num_of_staff = models.PositiveIntegerField(_("Number of Staff"), default=1, help_text=_("Numner of staffs that merchant can invite"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    can_upsell_teams = models.BooleanField(_("Upselling Subscription"), choices=((False, 'No'), (True, 'Yes')), default=False, help_text=_("Merchant with this package can sell subscription to their freelancers who want to upgrade"),)
    max_users_sitewide = models.PositiveIntegerField(_("Max number of users"), default=100, help_text=_("Total users including merchant and staffs"), validators=[MinValueValidator(100), MaxValueValidator(1000000)])
    multiple_freelancer_teams = models.BooleanField(_("Multiple teams per Freelancer"), choices=((False, 'No'), (True, 'Yes')), default=False, help_text=_("Each freelancer can create multiple teams"),)
    price = models.PositiveIntegerField(_("Package Price"), default=0, help_text=_("Decide your reasonable price with max limit of 1000"), validators=[MinValueValidator(0), MaxValueValidator(1000)])
    is_default = models.BooleanField(_("Make Default"), choices=((False, 'No'), (True, 'Yes')), help_text=_("Only 1 package should have a default set to 'Yes'"), default=False)
    ordering = models.PositiveIntegerField(_("Display"), default=1, help_text=_("This determines how each package will appear to user eg, 1 means first position"), validators=[MinValueValidator(1), MaxValueValidator(3)])
    # Upsell Configuration
    max_proposals_allowable_per_team = models.PositiveIntegerField(_("Max Proposals Per Team"), default=5, help_text=_("You can add min of 5 and max of 50 Proposals per Team"), validators=[MinValueValidator(5), MaxValueValidator(50)])
    monthly_projects_applicable_per_team = models.PositiveIntegerField(_("Monthly Applications Per Team"), default=10, help_text=_("Monthly Jobs Applications with min of 5 and max 50"), validators=[MinValueValidator(5), MaxValueValidator(50)])
    monthly_offer_contracts_per_team = models.PositiveIntegerField(_("Monthly Offer Contracts"), default=0, help_text=_("Clients can view team member's profile and send offer Contracts up to 100 monthly"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_member_per_team = models.PositiveIntegerField(_("Max Member per Team"), default=0, help_text=_("New feature Coming Soon: Here, freelancer team can send followup/ reminder mail per external contract to client. Daily sending will have min of 1 amd max is 3 mails"), validators=[MinValueValidator(0), MaxValueValidator(3)])
    upsell_price = models.PositiveIntegerField(_("Upsell Price"), default=0, help_text=_("Decide your reasonable price with max limit of 1000"), validators=[MinValueValidator(0), MaxValueValidator(1000)])

    def __str__(self):
        return str(self.verbose_type) if self.verbose_type else str(self.get_type_display())

    class Meta:
        ordering = ['ordering']


class Merchant(SettingsMaster):
    # Merchant Type
    EXEMPT = 1 # For special accounts that require no subscription
    BETA = 2 # For beta users
    TRIALING = 4 # For users who have been given a trial
    ACTIVE = 5
    PAST_DUE = 6
    CANCELED = 7
    TRIAL_EXPIRED = 8
    MERCHANT_TYPE = (
        (EXEMPT, _('Exempted')),
        (BETA, _('Beta')),
        (TRIALING, _('Trialing')),
        (ACTIVE, _('Active')),
        (PAST_DUE, _('Past Due')),
        (CANCELED, _('Canceled')),
        (TRIAL_EXPIRED, _('Trial Expired')),
    )

    MALE = 'male'
    FEMALE = 'female'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )    
    ACTIVE_TYPES = (EXEMPT, BETA, TRIALING, ACTIVE)
    PRE_PLAN_TYPES = (TRIALING, TRIAL_EXPIRED)
    END_TYPES = (CANCELED, TRIAL_EXPIRED)

    # Initial Plan Configuration
    type = models.PositiveIntegerField(_("Account Status"), choices=MERCHANT_TYPE, default=TRIALING)
    merchant = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='merchant', on_delete=models.CASCADE)
    business_name = models.CharField(_("Business Name"), max_length=255)
    domain = models.CharField(_("Default Domain"), max_length=255)
    package = models.ForeignKey("account.Package", 
        verbose_name=_("Package"), 
        related_name="packages",
        on_delete=models.PROTECT
    )
    package_expiry = models.DateTimeField(_("Package Expiry Date"), blank=True, null=True)
    gateways = models.ManyToManyField("payments.PaymentGateway", 
        verbose_name=_("Supported Gateways"),
        related_name="packages"
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Company Staff"), related_name="merchant_staff")    
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER)
    profile_photo = models.ImageField(_("Profile Photo"), upload_to='client/', default='client/avatar5.png')
    
    # Additional Customizations
    show_gateways = models.BooleanField(_("Display Gateway"), default=True)
    gateway_title = models.CharField(_("Gateway Title"), max_length=100, default="Collection and Payout Methods", null=True, blank=True)
    proposal_title = models.CharField(_("Div Three Proposal Title"), max_length=100, default="Explore Proposals", null=True, blank=True)
    proposal_subtitle = models.CharField(_("Div Three Proposal Subitle"), max_length=100, default="Verified Proposals", null=True, blank=True)
    project_title = models.CharField(_("Div Five Project Title"), max_length=100, default="Published Jobs", null=True, blank=True)
    project_subtitle = models.CharField(_("Div Five Project Subitle"), max_length=100, default="Apply and get Hired", null=True, blank=True)
    category_title = models.CharField(_("Div Two Category Title"), max_length=100, default="Explore Categories", null=True, blank=True)
    category_subtitle = models.CharField(_("Div Two Category Subitle"), max_length=100, default="Professional by categories", null=True, blank=True)
            

    def __str__(self):
        return str(self.business_name)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"

    def save(self, *args, **kwargs):
        self.domain = self.site.domain
        self.business_name = self.site.name
        super(Merchant, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.profile_photo))
    
    image_tag.short_description = 'profile_photo'


    @property
    def trial_end(self):
        """Calculate the account's trial end date."""
        return self.merchant.date_joined + datetime.timedelta(days=constant.TRIAL_DAYS)
    

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='twofactorauth', on_delete=models.CASCADE)
    pass_code = encrypt(models.CharField(_("Access Token"), max_length=255, blank=True, null=True))
    last_login = models.DateTimeField(_("Last Login"), auto_now=True)

    class Meta:
        ordering = ("-last_login",)
        verbose_name = "Access Token"
        verbose_name_plural = "Access Token"

    def __str__(self):
        return f'{self.user.get_full_name()}'    

    def save(self, *args, **kwargs):
        self.pass_code = auth_code()
        super(TwoFactorAuth, self).save(*args, **kwargs)
































