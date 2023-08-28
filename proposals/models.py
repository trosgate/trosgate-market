from django.core.files import File
from django.db import models
from django.db.models import Aggregate
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from contract.models import InternalContract
from django.urls import reverse
from django.utils.text import slugify
from merchants.models import MerchantProduct, MerchantMaster
from django.core.files.storage import FileSystemStorage
import uuid
from datetime import timedelta
from django.utils import timezone



PROTECTED_FILES_ROOT = settings.PROTECTED_MEDIA_ROOT
product_attachment = FileSystemStorage(location=str(PROTECTED_FILES_ROOT))


def proposal_images_path(instance, filename):
    return "proposal/%s/%s" % (instance.team.title, filename)

def product_storage(instance, filename):
    return f"product/{instance.team.title}/attachments/{filename}"


class Proposal(MerchantProduct):
    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'
    PRICING_TIERS = (
        (BASIC, _("Basic")),
        (STANDARD, _("Standard")),
        (PREMIUM, _("Premium")),
    )

    ONE_TIME = 1
    TWO_TIMES = 2
    THREE_TIMES = 3
    FOUR_TIMES = 4
    FIVE_TIMES = 5
    SIX_TIMES = 6
    SEVEN_TIMES = 7
    PRODUCT_CHOICES = (
        (ONE_TIME, _("1 Time")),
        (TWO_TIMES, _("2 Times")),
        (THREE_TIMES, _("3 Times")),
        (FOUR_TIMES, _("4 Times")),
        (FIVE_TIMES, _("5 Times")),
        (SIX_TIMES, _("6 Times")),
        (SEVEN_TIMES, _("7 Times")),
    )
    ONE_DAY = 1
    TWO_DAYS = 2
    THREE_DAYS = 3
    FOUR_DAYS = 4
    FIVE_DAYS = 5
    SIX_DAYS = 6
    ONE_WEEK = 7
    TWO_WEEK = 14
    THREE_WEEK = 21
    ONE_MONTH = 30
    PACKAGE_DURATION = (
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
    thumbnail = models.ImageField(_("Thumbnail"), help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to=proposal_images_path, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="proposalteam", on_delete=models.CASCADE, max_length=250)

    faq_one = models.CharField(_("FAQ #1"), max_length=100)
    faq_one_description = models.TextField(_("FAQ #1 Details"), max_length=255)
    faq_two = models.CharField(_("FAQ #2"), max_length=100, null=True, blank=True)
    faq_two_description = models.TextField(_("FAQ #2 Details"), max_length=255, null=True, blank=True)
    faq_three = models.CharField(_("FAQ #3"), max_length=100, null=True, blank=True)
    faq_three_description = models.TextField(_("FAQ #3 Details"), max_length=255, null=True, blank=True)
    
    digital = models.BooleanField(_("Digital Product"), choices=((False, 'No'), (True, 'Yes')), default=False)
    pricing = models.BooleanField(_("Tier Pricing"), choices=((False, 'No'), (True, 'Yes')), default=True)
    
    pricing_tier = models.CharField(_("Pricing Tier"), max_length=30, choices=PRICING_TIERS, default=BASIC)
    salary_tier1 = models.PositiveIntegerField(_("Price Tier1"), default=0)
    salary_tier2 = models.PositiveIntegerField(_("Price Tier2"), default=0)
    salary_tier3 = models.PositiveIntegerField(_("Price Tier3"), default=0)

    tier1_preview = models.CharField(_("Package 1 preview"), max_length=80, default='Features for Basic package', null=True, blank=True)
    tier2_preview = models.CharField(_("Package 2 preview"), max_length=80, default='Features for Standard package', null=True, blank=True)
    tier3_preview = models.CharField(_("Package 3 preview"), max_length=80, default='Features for Premium package', null=True, blank=True)

    revision_tier1 = models.PositiveIntegerField(_("Revision Tier1"), choices=PRODUCT_CHOICES, default=ONE_TIME)
    revision_tier2 = models.PositiveIntegerField(_("Revision Tier2"), choices=PRODUCT_CHOICES, default=THREE_TIMES)
    revision_tier3 = models.PositiveIntegerField(_("Revision Tier3"), choices=PRODUCT_CHOICES, default=SEVEN_TIMES)
    
    pricing1_duration = models.PositiveIntegerField(_("Duration Tier1"), choices=PACKAGE_DURATION, default=THREE_DAYS)       
    pricing2_duration = models.PositiveIntegerField(_("Duration Tier2"), choices=PACKAGE_DURATION, default=FIVE_DAYS)
    pricing3_duration = models.PositiveIntegerField(_("Duration Tier3"), choices=PACKAGE_DURATION, default=ONE_WEEK)       

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Proposal")
        verbose_name_plural = _("Proposals")
        unique_together = ['slug', 'merchant']

    def __str__(self):
        if self.pricing:
            return f'{self.title} - (Amount={self.salary}, Duration={self.get_pricing2_duration_display()})'
        else:
            return f'{self.title} - (Amount={self.salary}, Duration={self.get_duration_display()})'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.thumbnail))

    image_tag.short_description = 'thumbnail'

    # absolute url for proposal detail page
    def proposal_absolute_url(self):
        return reverse('proposals:proposal_preview', kwargs={'short_name': self.created_by.short_name, 'proposal_slug':self.slug})
    
    def proposal_detail_absolute_url(self):
        return reverse('proposals:proposal_detail', kwargs={'short_name': self.created_by.short_name, 'proposal_slug':self.slug})
    
    def tracking_time(self):
        return sum(tracker.minutes for tracker in self.trackings.all())

    def save(self, *args, **kwargs):
        if self.duration_time is None:
            self.duration_time = (timezone.now() + timedelta(days = self.duration))

        if not self.reference:
            self.reference = self.generate_unique_reference()

        self.slug=(slugify(self.title))
        
        if self.pricing == True:
            self.salary = self.salary_tier2

        super(Proposal, self).save(*args, **kwargs)


    def generate_unique_reference(self):
        max_attempts = 1000
        attempts = 0

        while attempts < max_attempts:
            # Generate a random UUID and convert it to a human-readable string
            # We set max_attempt to prevent function from going into potential infinite loop
            reference = str(uuid.uuid4()).replace('-', '')[:8].upper()

            # Check if the generated reference is unique
            if not Proposal.objects.filter(reference=reference).exists():
                return reference

            attempts += 1

        raise ValueError("Failed to create transaction")


    @property
    def preview_proposal_sales_count(self):
        return self.proposalhired.filter(purchase__status='success').count()


    @property
    def preview_contract_sales_count(self):
        new_contract = 0
        contracts = InternalContract.objects.filter(proposal__id=self.id)
        for contract in contracts:
            new_contract = contract.contracthired.filter(purchase__status='success').count()
        return new_contract


    @property
    def aggregated_sales_count(self):
        return (self.preview_proposal_sales_count + self.preview_contract_sales_count)


class ProposalProduct(MerchantMaster):
    id = models.AutoField(primary_key=True),
    license = models.URLField(editable=False, unique=True, default=uuid.uuid4, verbose_name='Product License')    
    team = models.ForeignKey('teams.Team', verbose_name=_("Product Team"), on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, verbose_name=_("Proposal"), on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), on_delete=models.CASCADE)
    product_type = models.BooleanField(_("Product Type"), choices=((False, 'Free Download'), (True, 'Premium Download')))
    status = models.BooleanField(_("Status"), choices=((False, 'Not Active'), (True, 'Active')))
    attachment = models.FileField(
        _("Attachment"), 
        help_text=_("image must be any of these 'ZIP', 'RAR','JPEG','JPG','PNG','PSD'"), 
        upload_to=product_storage, storage=product_attachment, validators=[FileExtensionValidator(allowed_extensions=['ZIP', 'RAR', 'JPG', 'JPEG', 'PNG', 'PSD'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField(_("Custom Price"), blank=True, null=True)
    
    class Meta:
        ordering = ('created_at',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together = ['product_type', 'proposal']

    def __str__(self):
        return f'{self.team.title}'

    def save(self, *args, **kwargs):
        if self.price is None or self.price == '' and self.product_type == True:
            self.price = self.proposal.salary
        if self.product_type == False:
            self.price = 0
        super(ProposalProduct, self).save(*args, **kwargs)

    def product_price(self):
        return f'{self.merchant.merchant.country.currency} {self.price}'


class ProposalSupport(Proposal):
    class Meta:
        proxy=True
        ordering = ['created_at']
        verbose_name = _("Proposal Support")
        verbose_name_plural = _("Proposal Support")


class ProposalChat(MerchantMaster):
    team = models.ForeignKey('teams.Team', verbose_name=_("Proposal Team"), related_name='proposalchats', on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, verbose_name=_("Proposal"), related_name='proposalschats', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='proposalsender', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return f'Message sent by {self.sender.get_full_name()}'






















