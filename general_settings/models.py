from pickle import FALSE
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core.cache import cache
import os
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django_cryptography.fields import encrypt
from django.core.exceptions import ValidationError


class WebsiteSetting(models.Model):
    USE_HTTPS = "https://"
    USE_HTTP = "http://"
    PROTOCOL_TYPE = (
        (USE_HTTPS, _("https://")),
        (USE_HTTP, _("http://")),
    )
    USE_WWW = "www"
    NO_WWW = "no_www"
    APPLY_WWW = (
        (USE_WWW, _("Use WWW")),
        (NO_WWW, _("No WWW")),
    )

    site_name = models.CharField(
        _("Site Name"), max_length=50, default="Example", null=True, blank=True)
    tagline = models.CharField(
        _("Site Tagline"), max_length=150, default="The Marketplace", null=True, blank=True)
    site_description = models.TextField(
        _("Site Decription"), max_length=300, default="The Example Marketplace", null=True, blank=True)
    site_Logo = models.ImageField(
        _("Site Logo"),  upload_to='site/', default='site/logo.png', null=True, blank=True)
    protocol = models.CharField(
        _("Protocol Type"), max_length=20, choices=PROTOCOL_TYPE, default=USE_HTTPS)
    use_www = models.BooleanField(_("Use WWW Url"), choices=((True, 'Use WWW'), (False, 'No WWW')), default=False)
    site_domain = models.CharField(_("Website Domain"), max_length=255, default="example.com", help_text=_(
        'E.x: example.com'), null=True, blank=True)
    site_url = models.URLField(_("Website URL"), help_text=_(
        'E.x: https://www.example.com'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'


    # image display in Admin

    def site_logo_tag(self):
        if self.site_Logo:
            return mark_safe('<img src="/media/%s" width="150" height="50" />' % (self.site_Logo))
        else:
            return (self.site_name)

    site_logo_tag.short_description = 'site_Logo'

    def get_site_logo(self):
        if self.site_Logo:
            return self.site_Logo.url
        else:
            return self.site_name


class StorageBuckets(models.Model):
    description = models.CharField(_("Storages"), max_length=100, default='Local Storage and Amazon S3 Configuration',)
    bucket_name = encrypt(models.CharField(_("Bucket Name"), max_length=100, null=True, blank=True,))
    access_key = encrypt(models.CharField(_("S3 Access Key"), max_length=100, null=True, blank=True,))
    secret_key = encrypt(models.CharField(_("S3 Secret Key"), max_length=100, null=True, blank=True,))
    storage_type = models.BooleanField(_("Storage Type"), choices=((True, 'Local Storage'), (False, 'Amazon S3 Bucket')), default=True)

    class Meta:
        verbose_name = 'File and Image Storage'
        verbose_name_plural = 'File and Image Storage'

    def __str__(self):
        return str(self.description)

    def clean(self):       
        if  self.storage_type == False and not (self.bucket_name is not None and self.access_key is not None and self.secret_key is not None):
            raise ValidationError(_("All extra Amazon S3 setting fields below are required to activate S3 Bucket."))


class TestEmail(models.Model):
    title = encrypt(models.CharField(_("Testing Email"), max_length=20, default="My Test Email", null=True, blank=True))
    test_email = encrypt(models.EmailField(_("Enter Email and Save to send"), max_length=100, help_text=_(
        "Test the email settings by sending a Test mail"), null=True, blank=True))

    def __str__(self):
        return f'Testing: {self.test_email}'

    class Meta:
        verbose_name = 'Test Email Settings'
        verbose_name_plural = 'Test Email'


class PaymentAPIs(models.Model):
    preview = models.CharField(_("Preamble"), max_length=255, default="This is the API Section for the integrated payment gateways", blank=True)
    gateway_count = models.PositiveSmallIntegerField(_("Number of Gateways"), default=4, blank=True, null=True)

    # Stripe API Credentials
    stripe_public_key = encrypt(models.CharField(_("STRIPE PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    stripe_secret_key = encrypt(models.CharField(_("STRIPE SECRET KEY"), max_length=255, blank=True, null=True))
    stripe_webhook_key = encrypt(models.CharField(_("STRIPE WEEBHOOK KEY(OPTIONAL)"), max_length=255, blank=True, null=True))
    stripe_subscription_price_id = encrypt(models.CharField(_("STRIPE SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    # PayPal API Credentials
    paypal_public_key = encrypt(models.CharField(_("PAYPAL PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    paypal_secret_key = encrypt(models.CharField(_("PAYPAL SECRET KEY"), max_length=255, blank=True, null=True))
    paypal_subscription_price_id = encrypt(models.CharField(_("PAYPAL SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    sandbox = models.BooleanField(_("Sandbox Mode"), choices=((False, 'No'), (True, 'Yes')), default=True)
    # Flutterwave API Credentials
    flutterwave_public_key = encrypt(models.CharField(_("FLUTTERWAVE PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    flutterwave_secret_key = encrypt(models.CharField(_("FLUTTERWAVE SECRET KEY"), max_length=255, blank=True, null=True))
    flutterwave_secret_hash = models.UUIDField(unique=True, verbose_name="Flutterwave secret Hash", editable=True, default=uuid.uuid4,)
    flutterwave_subscription_price_id = encrypt(models.CharField(_("FLUTTERWAVE SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))
    # Razorpay API Credentials
    razorpay_public_key_id = encrypt(models.CharField(_("RAZORPAY PUBLISHABLE KEY"), max_length=255, blank=True, null=True))
    razorpay_secret_key_id = encrypt(models.CharField(_("RAZORPAY SECRET KEY"), max_length=255, blank=True, null=True))
    razorpay_subscription_price_id = encrypt(models.CharField(_("RAZORPAY SUBSCRIPTION PRICE ID"), max_length=255, blank=True, null=True))

    def __str__(self):
        return self.preview

    class Meta:
        verbose_name = 'Payment API'
        verbose_name_plural = 'Payment API'

    def save(self, *args, **kwargs):
        self.gateway_count = 4
        super(PaymentAPIs, self).save(*args, **kwargs)


class AutoLogoutSystem(models.Model):
    # Auto Logout System
    preview = models.CharField(
        _("Preview"), max_length=50, default="Auto Logout System", blank=True)
    warning_time_schedule = models.PositiveIntegerField(_("Warning Time"), default="2", help_text=_(
        'By default the system will attempt to logout user every 2hrs with a prompt. You can change it in hours or days'), blank=True)
    interval = models.CharField(_("Extension Interval"), max_length=10, default="+2 Hours", help_text=_(
        'The period of time user can extend to remain logged-in before another warning'), blank=True)

    def __str__(self):
        return self.interval

    class Meta:
        verbose_name = 'Logout Control'
        verbose_name_plural = 'Logout Control'


class PaymentGateway(models.Model):
    name = models.CharField(_("Payment Gateway"), null=True, blank=True, max_length=255, help_text=_(
        "type of payment gateway e.g PayPal"), unique=True)
    status = models.BooleanField(_("Status"), choices=(
        (False, 'Inactive'), (True, 'Active')), default=False)
    processing_fee = models.PositiveIntegerField(_("Processing Fee"), null=True, blank=True, default=0, help_text=_(
        "discount price must be less than actual price"), validators=[MinValueValidator(0), MaxValueValidator(20000)])
    ordering = models.PositiveIntegerField(_("Ordering"), default=1, help_text=_(
        "This determines how each Gateway will appear to user eg, 1 means 1st position"), validators=[MinValueValidator(1), MaxValueValidator(10)])
    default = models.BooleanField(_("Default"), choices=(
        (False, 'No'), (True, 'Yes')), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering']


class SubscriptionGateway(models.Model):
    name = models.CharField(_("Payment Gateway"), null=True, blank=True, max_length=255, help_text=_(
        "type of payment gateway e.g PayPal"), unique=True)
    status = models.BooleanField(_("Status"), choices=(
        (False, 'Inactive'), (True, 'Active')), default=False)
    processing_fee = models.PositiveIntegerField(_("Processing Fee"), null=True, blank=True, default=0, help_text=_(
        "discount price must be less than actual price"), validators=[MinValueValidator(0), MaxValueValidator(20000)])
    ordering = models.PositiveIntegerField(_("Ordering"), default=1, help_text=_(
        "This determines how each Gateway will appear to user eg, 1 means 1st position"), validators=[MinValueValidator(1), MaxValueValidator(10)])
    default = models.BooleanField(_("Default"), choices=(
        (False, 'No'), (True, 'Yes')), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering']


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50, help_text=_(
        "Category field is Required"), unique=True, db_index=True)
    icon = models.ImageField(
        _("Icon"), upload_to='categories/', default='categories/category.png',)
    preview = models.TextField(_("Preview"), help_text=_(
        "Summarized info about your category"), max_length=60, null=True, blank=True,)
    visible = models.BooleanField(
        choices=((False, 'Private'), (True, 'Public')), default=False)
    slug = models.SlugField(_("Slug"), max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.icon))

    image_tag.short_description = 'icon'

    # absolute url for category detail page
    def category_absolute_url(self):
        return reverse('general_settings:category', args=[self.slug])


class Department(models.Model):
    name = models.CharField(_("Department Name"), max_length=100, help_text=_(
        "Department field is Required"), unique=True, blank=True)

    class Meta:
        verbose_name = 'Client Department'
        verbose_name_plural = 'Clients Department'

    def __str__(self):
        return f'{self.name}'



class Size(models.Model):
    size = models.CharField(_("Business Size"), max_length=100, help_text=_(
        "Business Size field is Required"), unique=True, blank=True)

    class Meta:
        verbose_name = 'Business Size'
        verbose_name_plural = 'Business Sizes'

    def __str__(self):
        return f'{self.size}'


class Skill(models.Model):
    name = models.CharField(_("Skill"), max_length=100, help_text=_(
        "Skill field is Required"), unique=True, blank=True)

    def __str__(self):
        return self.name


class CommunicationLanguage(models.Model):
    language = models.CharField(_("User Communication Language"), max_length=100, help_text=_(
        "User Communication Language Required"), unique=True)

    def __str__(self):
        return self.language


class ProposalGuides(models.Model):
    guide = models.CharField(_("guide"), max_length=100, help_text=_(
        "Instructions you want to show to customers"), unique=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Instruction")
        verbose_name_plural = _("Instructions")

    def __str__(self):
        return self.guide


class DiscountSystem(models.Model):
    preview = models.CharField(
        _("Preview"), max_length=50, default="Level Based Discount System")
    level_one_name = models.CharField(
        _("Level One(L1)"), max_length=30, default="Level One Discount System", unique=True)
    level_one_rate = models.PositiveIntegerField(_("L1 Rate"), default=0, help_text=_(
        "Starting Rate for L1 Discount with minimum default of 0 %"), validators=[MinValueValidator(0), MaxValueValidator(0)])
    level_one_start_amount = models.PositiveIntegerField(_("L1 Amount Start"), default=0, help_text=_(
        "Minimum checkout amount with default of zero(0) currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])
    level_one_delta_amount = models.PositiveIntegerField(_("L1 Amount Delta"), default=199, help_text=_(
        "checkout amount delta with default of 199 currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])

    level_two_name = models.CharField(
        _("Level Two(L2)"), max_length=30, default="Level Two Discount System", unique=True)
    level_two_rate = models.PositiveIntegerField(_("L2 Rate"), default=3, help_text=_(
        "Second level Rate for L2 Discount with minimum default of 3%"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    level_two_start_amount = models.PositiveIntegerField(_("L2 Amount Start"), default=300, help_text=_(
        "Minimum checkout amount with default of 300 currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])
    level_two_delta_amount = models.PositiveIntegerField(_("L2 Amount Delta"), default=499, help_text=_(
        "checkout amount delta with default of 499 currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])

    level_three_name = models.CharField(
        _("Level Three(L3)"), max_length=30, default="Level Three Discount System", unique=True)
    level_three_rate = models.PositiveIntegerField(_("L3 Rate"), default=5, help_text=_(
        "Medium Rate for L3 Discount with minimum default of 5%"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    level_three_start_amount = models.PositiveIntegerField(_("L3 Amount Start"), default=500, help_text=_(
        "Minimum checkout amount with default of 500 currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])
    level_three_delta_amount = models.PositiveIntegerField(_("L3 Amount Delta"), default=999, help_text=_(
        "checkout amount delta with default of 999 currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])

    level_four_name = models.CharField(
        _("Level Four(L4)"), max_length=30, default="Level Four Discount System", unique=True)
    level_four_rate = models.PositiveIntegerField(_("L4 Rate"), default=7, help_text=_(
        "Highest Rate for L4 Discount with minimum default of 7%"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    level_four_start_amount = models.PositiveIntegerField(_("L4 Amount Start"), default=1000, help_text=_(
        "Minimum checkout Amount with default of 1000 currency points"), validators=[MinValueValidator(0), MaxValueValidator(50000)])

    class Meta:
        verbose_name = _("Discount Level System")
        verbose_name_plural = _("Discount Level System")

    def __str__(self):
        return self.preview

    def level_one_discount(self):
        return f'{self.level_one_rate}%'

    def level_two_discount(self):
        return f'{self.level_two_rate}%'

    def level_three_discount(self):
        return f'{self.level_three_rate}%'

    def level_four_discount(self):
        return f'{self.level_four_rate}%'

    def clean(self):
        # Start amount against delta validation
        if self.level_one_start_amount >= self.level_one_delta_amount:
            raise ValidationError(
                {'level_one_start_amount': _('L1 Amount Start cannot be bigger than L1 Amount Delta')})
        
        if self.level_two_start_amount >= self.level_two_delta_amount:
            raise ValidationError(
                {'level_two_start_amount': _('L2 Amount Start cannot be bigger than L2 Amount Delta')})
        
        if self.level_three_start_amount >= self.level_three_delta_amount:
            raise ValidationError(
                {'level_three_start_amount': _('L3 Amount Start cannot be bigger than L3 Amount Delta')})
        
        if self.level_four_start_amount < self.level_three_start_amount or self.level_four_start_amount < self.level_two_start_amount or self.level_four_start_amount < self.level_one_start_amount:
            raise ValidationError(
                {'level_four_start_amount': _('L4 Amount Start must be the biggest of all levels start amount')})
        
        # Rate against other rates validation
        if self.level_one_rate > self.level_two_rate or self.level_one_rate > self.level_three_rate or self.level_one_rate > self.level_four_rate:
            raise ValidationError(
                {'level_one_rate': _('L1 Rate must be the smallest of all 4 level rates')})
        
        if self.level_two_rate > self.level_three_rate or self.level_two_rate > self.level_four_rate:
            raise ValidationError(
                {'level_two_rate': _('L2 Rate must be the second lowest rate after L1 level rate')})
        
        if self.level_three_rate > self.level_four_rate:
            raise ValidationError(
                {'level_three_rate': _('L3 Rate must be the third lowest rate after L1 and L2 rate')})
        
        # Start amount vrs delta validation
        if self.level_one_delta_amount >= self.level_two_start_amount:
            raise ValidationError(
                {'level_one_delta_amount': _('L1 Amount delta cannot be bigger or equal to L2 Amount Start')})
                        
        if self.level_two_delta_amount >= self.level_three_start_amount:
            raise ValidationError(
                {'level_two_delta_amount': _('L2 Amount delta cannot be bigger or equal to L3 Amount Start')})
        
        if self.level_three_delta_amount >= self.level_four_start_amount:
            raise ValidationError(
                {'level_three_delta_amount': _('L3 Amount delta cannot be bigger or equal to L4 Amount Start')})
                        
        return super().clean()



class HiringFee(models.Model):
    preview = models.CharField(
        _("Freelancer fees and charges"), max_length=50, default="Freelancer fees and charges")
    # Contract fee and charges
    extcontract_fee_percentage = models.PositiveIntegerField(_("External Contract Fee - (%)"), default=20, help_text=_(
        "This is the first and final percentage fee per external contract"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    contract_fee_percentage = models.PositiveIntegerField(_("Contract Fee - (%)"), default=20, help_text=_(
        "This is the first percentage fee per contract up to Break-Point amount"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    contract_fee_extra = models.PositiveIntegerField(_("Contract Extra Fee - (%)"), default=5, help_text=_(
        "An extra percentage contract fee charged beyond Break-Point amount"), validators=[MinValueValidator(0), MaxValueValidator(70)])
    contract_delta_amount = models.PositiveIntegerField(_("Contract Break-Point (Value)"), default=300, help_text=_(
        "The break-point for charging extra Contract fee on freelancer total earning"), validators=[MinValueValidator(0), MaxValueValidator(50000)])
    # Proposal fee and charges
    proposal_fee_percentage = models.PositiveIntegerField(_("Proposal Fee - (%)"), default=20, help_text=_(
        "This is the first percentage fee per proposal up to Break-Point amount"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    proposal_fee_extra = models.PositiveIntegerField(_("Proposal Extra Fee - (%)"), default=5, help_text=_(
        "An extra percentage Proposal fee charged beyond Break-Point amount"), validators=[MinValueValidator(0), MaxValueValidator(70)])
    proposal_delta_amount = models.PositiveIntegerField(_("Proposal Break-Point (Value)"), default=300, help_text=_(
        "The break-point for charging extra Proposal fee on freelancer total earning"), validators=[MinValueValidator(0), MaxValueValidator(50000)])
    # Project fee and charges
    application_fee_percentage = models.PositiveIntegerField(_("Job Applicant Fee - (%)"), default=20, help_text=_(
        "This is the first percentage fee per project applied up to Break-Point amount"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    application_fee_extra = models.PositiveIntegerField(_("Job Applicant Extra Fee - (%)"), default=5, help_text=_(
        "An extra percentage project hiring fee charged beyond Break-Point amount"), validators=[MinValueValidator(0), MaxValueValidator(70)])
    application_delta_amount = models.PositiveIntegerField(_("Job Applicant Break-Point (Value)"), default=300, help_text=_(
        "The break-point for charging extra project hiring fee on freelancer total earning"), validators=[MinValueValidator(0), MaxValueValidator(50000)])

    class Meta:
        verbose_name = _("Hiring Fee System")
        verbose_name_plural = _("Hiring Fee System")

    def __str__(self):
        return self.preview

    def contract_percentage(self):
        return f'{self.contract_fee_percentage}% + {self.contract_fee_extra}%'

    def proposal_percentage(self):
        return f'{self.proposal_fee_percentage}% + {self.proposal_fee_extra}%'

    def application_percentage(self):
        return f'{self.application_fee_percentage}% + {self.application_fee_extra}%'


class Currency(models.Model):
    name = models.CharField(_("Currency Name"), max_length=100)
    code = models.CharField(_("Code"), max_length=10, default="USD")
    symbol = models.CharField(_("Currency"), max_length=10)
    supported = models.BooleanField(_("Supported"), choices=(
        (False, 'No'), (True, 'Yes')), default=True)
    ordering = models.PositiveIntegerField(
        _("Order Priority"), null=True, blank=True)
    default = models.BooleanField(_("Default"), choices=(
        (False, 'No'), (True, 'Yes')), blank=True)

    class Meta:
        ordering = ["ordering"]
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f'{self.name} - {self.code}'


class CurrencyConverter(models.Model):
    currency = models.ForeignKey(Currency, verbose_name=_(
        "Currency Type"), related_name="currencyconverter", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Currency Converter")
        verbose_name_plural = _("Currency Converter")

    def __str__(self):
        return self.currency.name

    # Api call from https://v6.exchangerate-api.com/


class ExachangeRateAPI(models.Model):
    preview = models.CharField(
        _("Preamble"), 
        max_length=100, 
        default="Exchange rate API", 
        blank=True, 
        null=True)
    exchange_rates_api_key = encrypt(models.CharField(
        _("API Key"), 
        max_length=255, 
        help_text=_('grab your key from https://exchangerate-api.com/'), 
        blank=True, 
        null=True))

    class Meta:
        verbose_name = _("Exchange Rates API")
        verbose_name_plural = _("Exchange Rates API")

    def __str__(self):
        return self.preview


class PaymentsControl(models.Model):
    preview = models.CharField(_("Payment Settings"), max_length=50,
                               default="All about Transfer and Withdrawal configuration")
    min_balance = models.PositiveIntegerField(_("Minimum T/W Balance"), default=0, help_text=_(
        "After making transfer or withdrawal, User account cannot fall below this limit $(0 - 200)"), validators=[MinValueValidator(0), MaxValueValidator(200)])
    max_receiver_balance = models.PositiveIntegerField(_("Maximum Receiver Balance"), default=2000, help_text=_(
        "After making transfer, RECEIVER account cannot fall above this limit $(201 - 2000)"), validators=[MinValueValidator(201), MaxValueValidator(2100)])
    min_transfer = models.PositiveIntegerField(_("Minimum Transfer"), default=20, help_text=_(
        "Minimum amount Team Owner/Freelancer can transfer per transaction - $(20 - 200)"), validators=[MinValueValidator(20), MaxValueValidator(200)])
    max_transfer = models.PositiveIntegerField(_("Maximum Transfer"), default=500, help_text=_(
        "Maximum amount Team Owner/Freelancer can transfer per transaction - $(201 - 2000)"), validators=[MinValueValidator(201), MaxValueValidator(2100)])
    min_withdrawal = models.PositiveIntegerField(_("Minimum Withdrawal"), default=20, help_text=_(
        "Minimum Amont freelancer can withdraw per transaction - $(20 - 200)"), validators=[MinValueValidator(20), MaxValueValidator(200)])
    max_withdrawal = models.PositiveIntegerField(_("Maximum Withdrawal"), default=500, help_text=_(
        "Maximum Amont freelancer can withdraw per transaction - $(201 - 2000)"), validators=[MinValueValidator(201), MaxValueValidator(2100)])

    class Meta:

        verbose_name = _("Payment Settings")
        verbose_name_plural = _("Payment Settings")

    def __str__(self):
        return self.preview


class DepositControl(models.Model):
    preview = models.CharField(
        _("Deposit Settings"), 
        max_length=50, 
        default="All about Deposit configuration")
    min_balance = models.PositiveIntegerField(
        _("Minimum Balance"), 
        default=0, 
        help_text=_("User with this minimum balance qualifies to make deposit (restricted to base Zero currency point"), 
        validators=[MinValueValidator(0)])
    max_balance = models.PositiveIntegerField(
        _("Maximum Balance"), 
        default=2000, 
        help_text=_("User with this Maximum balance has reached the max limit for further deposit(restricted to 50000 currency points)"), 
        validators=[MaxValueValidator(50000)])
    min_deposit = models.PositiveIntegerField(
        _("Minimum Deposit Amount"), 
        default=20, 
        help_text=_("Minimum mount client can deposit - (restricted to 20 minimum currency points)"), 
        validators=[MinValueValidator(20)])
    max_deposit = models.PositiveIntegerField(
        _("Maximum Deposit Amount"), 
        default=500, 
        help_text=_("Maximum amount client can deposit"), 
        validators=[MaxValueValidator(50000)])

    class Meta:

        verbose_name = _("Deposit Settings")
        verbose_name_plural = _("Deposit Settings")

    def __str__(self):
        return self.preview

        
class Payday(models.Model):
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
    PAYDAY_DURATION = (
        (ONE_DAY, _("01 Day")),
        (TWO_DAYS, _("02 Days")),
        (THREE_DAYS, _("03 Days")),
        (FOUR_DAYS, _("04 Days")),
        (FIVE_DAYS, _("05 Days")),
        (SIX_DAYS, _("06 Days")),
        (ONE_WEEK, _("01 Week")),
        (TWO_WEEK, _("02 Weeks")),
        (THREE_WEEK, _("03 Weeks")),
        (ONE_MONTH, _("01 Month")),
    )  
    preview = models.CharField(_("Preview"), max_length=100, default = 'Payday Timelines that users should expect money', help_text=_('"01 Week" means 7 Days, "02 Weeks" means 14 Days, "03 Weeks" means 21 Days, "01 Month" means 28-30 Days'))
    payday_converter = models.CharField(_("Duration"), max_length=20, choices=PAYDAY_DURATION, default = THREE_DAYS)

    class Meta:
        verbose_name = 'Payday Setting'
        verbose_name_plural = 'Payday Setting'

    def __str__(self):
        return f'{self.preview}'


class Mailer(models.Model):
   # Email API
    email_hosting_server = encrypt(models.CharField(
        _("Email Hosting Server"), 
        max_length=255,
        default="smtp.gmail.com", 
        help_text=_("E.x: smtp.gmail.com"), 
        null=True, 
        blank=True))
    email_hosting_server_password = encrypt(models.CharField(
        _("Email Server Password"), 
        max_length=255, 
        default='ngnrfcsozfrxbgfx', null=True, blank=True))
    email_hosting_username = encrypt(models.CharField(
        _("Email Server Username"), 
        max_length=255, 
        help_text=_('This is the email hosting username created'), 
        null=True, 
        blank=True))
    from_email = encrypt(models.CharField(
        _("From Email"), 
        max_length=255, help_text=_('This email will be the site-wide sender email'), 
        null=True, 
        blank=True))
    email_use_tls = encrypt(models.BooleanField(
        _("Use TLS"), 
        choices=((False, 'No'), (True, 'Yes')), 
        default=True, 
        help_text=_('If your hosting support both SSL and TLS, we recommend the use of TLS'), 
        null=True, 
        blank=True))
    email_use_ssl = encrypt(models.BooleanField(
        _("Use SSL"), 
        choices=((False, 'No'), (True, 'Yes')), 
        default=False, 
        help_text=_('If SSL is set to "Yes", TLS should be "No", and vise-versa'), 
        null=True, 
        blank=True))
    email_fail_silently = encrypt(models.BooleanField(
        _("Email Fail Silently"), 
        choices=((False, 'Show Error'), (True, 'Hide Error')), 
        default=True, 
        help_text=_('if you want users to see errors with your misconfiguration, set to "Show Error". We recommend that you Hide Error'), 
        null=True, 
        blank=True))
    email_hosting_server_port = models.PositiveSmallIntegerField(
        _("Email Server Port"), 
        default=587, 
        help_text=_('Usually 587 but confirm from your hosting company'), 
        null=True, 
        blank=True)
    email_timeout = models.PositiveSmallIntegerField(
        _("Email Timeout"), 
        default=60, 
        help_text=_('the timeout time for email'), 
        null=True,
        blank=True)

    def __str__(self):
        return f'{self.from_email}'

    class Meta:
        verbose_name = 'Mailer Settings'
        verbose_name_plural = 'Mailer Settings'

    def clean(self):
        if self.email_use_tls and self.email_use_ssl:
            raise ValidationError(
                _("\"Use TLS\" and \"Use SSL\" are mutually exclusive, "
                  "so only set one of those settings to Yes."))


__all__ = ['Mailer']
