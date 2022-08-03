from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from uuid import uuid4
from django.conf import settings
from proposals.utilities import (
    one_day, 
    two_days, 
    three_days, 
    four_days, 
    five_days, 
    six_days, 
    one_week,
    two_weeks,
    three_weeks,
    one_month,
    two_months,
    three_months,
    four_months,
    five_months,
    six_months
)


class InternalContract(models.Model):
    """
    This is the Internal contract Model
    """    
    # Internal Contract Duration
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
    CONTRACT_DURATION = (
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
        (TWO_MONTH, _("02 Months")),
        (THREE_MONTH, _("03 Months")),
        (FOUR_MONTH, _("04 Months")),
        (FIVE_MONTH, _("05 Months")),
        (SIX_MONTH, _("06 Months")),
    )   
    #
    # Invoice States
    PENDING = 'unpaid'
    PAID = 'paid'
    STATUS = (
        (PENDING, _('Unpaid')),
        (PAID, _('Paid')),
    )  
    #states 
    AWAITING = 'awaiting'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATE = (
        (AWAITING, _('Awaiting')),
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected')),
    )   
  
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="internalcontractteam", on_delete=models.CASCADE)
    proposal = models.ForeignKey('proposals.Proposal', verbose_name=_("Proposal"), related_name="internalcontractproposal", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), null=True, blank=True, related_name="internalcontractauthor", on_delete=models.SET_NULL)
    date_created = models.DateTimeField(_('Created On'),blank=True, null=True, default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True, default=timezone.now)
    contract_duration = models.CharField(_('Duration'), choices=CONTRACT_DURATION, default=ONE_DAY, max_length=20)
    duration = models.DateTimeField(_("Completion In"), blank=True, help_text=_("deadline for contract"))
    status = models.CharField(_('Status'), choices=STATUS, default=PENDING, max_length=30)
    team_reaction = models.CharField(_('State'), choices=STATE, default=AWAITING, max_length=30)
    notes = models.TextField(null=True, blank=True, max_length=500)

    reference = models.CharField(_('Reference'), unique=True, null=True, blank=True, max_length=100)
    urlcode = models.CharField(unique=True, null=True, blank=True, max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    line_one = models.CharField(_('Service Description'), max_length=120, default=None, blank=True, null=True)
    line_one_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_one_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_one_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    line_two = models.CharField('Service Extras One', max_length=120, default=None, blank=True, null=True)
    line_two_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_two_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_two_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    line_three = models.CharField('Service Extras Two', max_length=120, default=None, blank=True, null=True)
    line_three_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_three_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_three_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    line_four = models.CharField('Service Extras Three', max_length=120, default=None, blank=True, null=True)
    line_four_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_four_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_four_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)  

    line_five = models.CharField('Service Extras Four', max_length=120, default=None, blank=True, null=True)
    line_five_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_five_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_five_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    grand_total = models.PositiveIntegerField(_('Grand Total'), default=0, blank=True, null=True)  
     
    
    def __str__(self):
        return self.proposal.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("Internal Contract")
        verbose_name_plural = _("Internal Contracts")

    def get_internal_contract_detail_absolute_url(self):
        return reverse('contract:internal_contract_detail', args=[self.pk])

    def get_redeem_internal_contract_absolute_url(self):
        return reverse('contract:internal_contract_fee_structure', args=[self.slug])

    def save(self, *args, **kwargs):
        if self.urlcode is None:
            self.urlcode = str(uuid4())
        if self.reference is None:
            self.reference = 'In-' + str(uuid4()).split('-')[4]
        self.slug = slugify(self.proposal.title)

        if self.contract_duration == self.ONE_DAY:
            self.duration = one_day()
        elif self.contract_duration == self.TWO_DAYS:
            self.duration = two_days()
        elif self.contract_duration == self.THREE_DAYS:
            self.duration = three_days()
        elif self.contract_duration == self.FOUR_DAYS:
            self.duration = four_days()
        elif self.contract_duration == self.FIVE_DAYS:
            self.duration = five_days()
        elif self.contract_duration == self.SIX_DAYS:
            self.duration = six_days()
        elif self.contract_duration == self.ONE_WEEK:
            self.duration = one_week()
        elif self.contract_duration == self.TWO_WEEK:
            self.duration = two_weeks()
        elif self.contract_duration == self.THREE_WEEK:
            self.duration = three_weeks()
        elif self.contract_duration == self.ONE_MONTH:
            self.duration = one_month()
        elif self.contract_duration == self.TWO_MONTH:
            self.duration = two_months()
        elif self.contract_duration == self.THREE_MONTH:
            self.duration = three_months()
        elif self.contract_duration == self.FOUR_MONTH:
            self.duration = four_months()
        elif self.contract_duration == self.FIVE_MONTH:
            self.duration = five_months()
        elif self.contract_duration == self.SIX_MONTH:
            self.duration = six_months()
        super(InternalContract, self).save(*args, **kwargs)        


class Contractor(models.Model):
    """
    This is the external client to be invited
    """
    name = models.CharField(blank=True, max_length=100)
    email = models.CharField(max_length=100)
    reference = models.CharField(blank=True, max_length=100)
    address = models.CharField(null=True, blank=True, max_length=150)
    postal_code = models.CharField(null=True, blank=True, max_length=6)
    phone_Number = models.CharField(null=True, blank=True, max_length=100)
    tax_Number = models.CharField(null=True, blank=True, max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="contractors", on_delete=models.PROTECT)
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="contractors", on_delete=models.CASCADE)    

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("External Contractor")
        verbose_name_plural = _("External Contractor")

    def save(self, *args, **kwargs):
        if self.reference is None:
            self.reference = str(uuid4()).split('-')[4]       
        super(Contractor, self).save(*args, **kwargs)


class Contract(models.Model):
    """
    This is the external contract to be shared with contractor
    """
    # contract Duration
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
    CONTRACT_DURATION = (
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
        (TWO_MONTH, _("02 Months")),
        (THREE_MONTH, _("03 Months")),
        (FOUR_MONTH, _("04 Months")),
        (FIVE_MONTH, _("05 Months")),
        (SIX_MONTH, _("06 Months")),
    )   
    #
    # Invoice States
    PENDING = 'pending'
    PAID = 'paid'
    STATUS = (
        (PENDING, _('Pending')),
        (PAID, _('Paid')),
    )  
    #
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="contractsteam", on_delete=models.CASCADE)
    client = models.ForeignKey(Contractor, verbose_name=_("External Client"), related_name="contractsclient", blank=True, on_delete=models.PROTECT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), blank=True, related_name="contractsauthor", on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    contract_duration = models.CharField(_('Completion Time'), choices=CONTRACT_DURATION, default=ONE_DAY, max_length=20)
    status = models.CharField(choices=STATUS, default=PENDING, max_length=10)
    notes = models.TextField(null=True, blank=True, max_length=500)

    reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
    urlcode = models.CharField(unique=True, null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    
    line_one = models.CharField(_('Service Description'), max_length=120, default=None, blank=True, null=True)
    line_one_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_one_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_one_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    line_two = models.CharField('Service Extras One', max_length=120, default=None, blank=True, null=True)
    line_two_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_two_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_two_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    line_three = models.CharField('Service Extras Two', max_length=120, default=None, blank=True, null=True)
    line_three_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_three_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_three_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    line_four = models.CharField('Service Extras Three', max_length=120, default=None, blank=True, null=True)
    line_four_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_four_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_four_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)  

    line_five = models.CharField('Service Extras Four', max_length=120, default=None, blank=True, null=True)
    line_five_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
    line_five_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
    line_five_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

    grand_total = models.PositiveIntegerField(_('Grand Total'), default=0, blank=True, null=True)  
      
    
    def __str__(self):
        return self.team.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("External Contract")
        verbose_name_plural = _("External Contract")


    def get_contract_detail_absolute_url(self):
        return reverse('contract:contract_single', args=[self.id])


    def get_redeem_contract_absolute_url(self):
        return reverse('contract:redeem_contract', args=[self.id])


    def save(self, *args, **kwargs):
        if self.urlcode is None:
            self.urlcode = str(uuid4())
        if self.reference is None:
            self.reference = 'Ex-' + str(uuid4()).split('-')[4]
        self.slug = slugify(self.line_one)
        super(Contract, self).save(*args, **kwargs)


class InternalContractChat(InternalContract):
    class Meta:
        proxy=True


class ContractChat(models.Model):
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="contractteamchat", on_delete=models.PROTECT)
    contract = models.ForeignKey(InternalContract, verbose_name=_("External Client"), related_name="contractclientchat", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='contractchatsender', on_delete=models.PROTECT)    
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.team.title

    class Meta:
        ordering = ['sent_on']
        verbose_name = _("Contract Chat")
        verbose_name_plural = _("Contract Chat")
























