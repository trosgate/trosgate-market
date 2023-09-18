from django.db import models, transaction as db_transaction
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid
from django.conf import settings
from account.fund_exception import ContractException
from account.models import Customer
from notification.mailer import send_contract_accepted_email, send_contract_rejected_email
from merchants.models import MerchantMaster



# class InternalContract(models.Model):
#     """
#     This is the Internal contract Model
#     """    
#     # Internal Contract Duration
#     ONE_DAY = "one_day"
#     TWO_DAYS = "two_days"
#     THREE_DAYS = "three_days"
#     FOUR_DAYS = "four_days"
#     FIVE_DAYS = "five_days"
#     SIX_DAYS = "six_days"
#     ONE_WEEK = "one_week"
#     TWO_WEEK = "two_weeks"
#     THREE_WEEK = "three_weeks"
#     ONE_MONTH = "one_month"
#     TWO_MONTH = "two_month"
#     THREE_MONTH = "three_months"
#     FOUR_MONTH = "four_months"
#     FIVE_MONTH = "five_months"
#     SIX_MONTH = "six_months"
#     CONTRACT_DURATION = (
#         (ONE_DAY, _("01 Day")),
#         (TWO_DAYS, _("02 Days")),
#         (THREE_DAYS, _("03 Days")),
#         (FOUR_DAYS, _("04 Days")),
#         (FIVE_DAYS, _("05 Days")),
#         (SIX_DAYS, _("06 Days")),
#         (ONE_WEEK, _("01 Week")),
#         (TWO_WEEK, _("02 Weeks")),
#         (THREE_WEEK, _("03 Weeks")),
#         (ONE_MONTH, _("01 Month")),
#         (TWO_MONTH, _("02 Months")),
#         (THREE_MONTH, _("03 Months")),
#         (FOUR_MONTH, _("04 Months")),
#         (FIVE_MONTH, _("05 Months")),
#         (SIX_MONTH, _("06 Months")),
#     )   
#     #
#     #states 
#     AWAITING = 'awaiting'
#     ACCEPTED = 'accepted'
#     REJECTED = 'rejected'
#     PAID = 'paid'
#     STATE = (
#         (AWAITING, _('Awaiting')),
#         (ACCEPTED, _('Accepted')),
#         (REJECTED, _('Rejected')),
#         (PAID, _('Paid')),
#     )   
  
#     team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="internalcontractteam", on_delete=models.CASCADE)
#     proposal = models.ForeignKey('proposals.Proposal', verbose_name=_("Proposal"), related_name="internalcontractproposal", on_delete=models.CASCADE)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="internalcontractauthor", on_delete=models.CASCADE)
#     contract_duration = models.CharField(_('Duration'), choices=CONTRACT_DURATION, default=ONE_DAY, max_length=20)
#     reaction = models.CharField(_('State'), choices=STATE, default=AWAITING, max_length=30)
#     notes = models.TextField(null=True, blank=True, max_length=250)

#     reference = models.CharField(_('Reference'), unique=True, blank=True, max_length=100)
#     slug = models.SlugField(_('Slug'), blank=True, max_length=350)
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)
    
#     line_one = models.CharField(_('Service Description'), max_length=120)
#     line_one_quantity = models.PositiveIntegerField(_('Quantity'), default=0)
#     line_one_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0)
#     line_one_total_price = models.PositiveIntegerField(_('Total'), default=0)

#     line_two = models.CharField('Service Extras One', max_length=120, default=None, blank=True, null=True)
#     line_two_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
#     line_two_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
#     line_two_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

#     line_three = models.CharField('Service Extras Two', max_length=120, default=None, blank=True, null=True)
#     line_three_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
#     line_three_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
#     line_three_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

#     line_four = models.CharField('Service Extras Three', max_length=120, default=None, blank=True, null=True)
#     line_four_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
#     line_four_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
#     line_four_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)  

#     line_five = models.CharField('Service Extras Four', max_length=120, default=None, blank=True, null=True)
#     line_five_quantity = models.PositiveIntegerField(_('Quantity'), default=0, blank=True, null=True)
#     line_five_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0, blank=True, null=True)
#     line_five_total_price = models.PositiveIntegerField(_('Total'), default=0, blank=True, null=True)

#     grand_total = models.PositiveIntegerField(_('Grand Total'), default=0, blank=True, null=True)  
        
#     def __str__(self):
#         return self.proposal.title

#     class Meta:
#         ordering = ['-date_created']
#         verbose_name = _("Internal Contract")
#         verbose_name_plural = _("Internal Contracts")

#     def get_internal_contract_detail_absolute_url(self):
#         return reverse('contract:internal_contract_detail', args=[self.pk])

#     def get_redeem_internal_contract_absolute_url(self):
#         return reverse('contract:internal_contract_fee_structure', args=[self.slug])


#     @classmethod
#     def capture(cls, pk:int, reaction):
#         with db_transaction.atomic():
#             contract = cls.objects.select_for_update().get(pk=pk)
#             if contract.reaction != 'awaiting':
#                 raise ContractException('Contract must be in awaiting state to accept or reject')
            
#             contract.reaction = reaction
#             contract.save()

#             # if contract.reaction == 'accepted':
#             #     db_transaction.on_commit(lambda: send_contract_accepted_email(contract))
            
#             # if contract.reaction == 'rejected':
#             #     db_transaction.on_commit(lambda: send_contract_rejected_email(contract))
 
#         return contract
        

class Contractor(MerchantMaster):
    """
    This is the external client to be invited
    """
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, help_text=_("Enter an official name known for the client"))
    email = models.CharField(max_length=100, help_text=_("Enter Valid Email for client to receive mail"), unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Invitee"), related_name="contractors", on_delete=models.CASCADE)
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="contractors", on_delete=models.CASCADE)    

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("External Client")
        verbose_name_plural = _("External Client")
        unique_together = ['email', 'team']


    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(Contractor, self).save(*args, **kwargs)

    @property
    def is_connected(self):
        if self.contracts.filter(client__email=self.email).exists():
            return True
        else:
            return False

    @classmethod
    def add_client(cls, name, email, team, created_by):
        if not name:
            raise Exception("Client's name required")
        if not email:
            raise Exception("Client's email required")
        if cls.objects.filter(Q(email__iexact=email)).exists():
            raise Exception("This client already exists. Add different person")
        if Customer.objects.filter(Q(user_type='client', email__iexact=email)).exists():
            raise Exception("Sorry! Let this client login and offer you contract")
        
        client = cls.objects.create(name=name, 
            email=email, 
            team=team, 
            created_by=created_by
        )
        return client


class Contract(MerchantMaster):
    """
    This is the Contract Model
    """
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
    TWO_MONTH = 60
    THREE_MONTH = 90
    FOUR_MONTH = 120
    FIVE_MONTH = 150
    SIX_MONTH = 180
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

    #Types 
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    TYPES = (
        (INTERNAL, _('Internal')),
        (EXTERNAL, _('External')),
    )

    #states 
    AWAITING = 'awaiting'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    PAID = 'paid'
    STATE = (
        (AWAITING, _('Awaiting')),
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected')),
        (PAID, _('Paid')),
    )   

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="contracts", on_delete=models.CASCADE)
    client = models.ForeignKey(Contractor, verbose_name=_("External Client"), related_name="contracts", blank=True,null=True, on_delete=models.CASCADE)
    proposal = models.ForeignKey('proposals.Proposal', verbose_name=_("Proposal"), related_name="contracts", blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), blank=True, related_name="contractsauthor", on_delete=models.CASCADE)
    contract_duration = models.PositiveIntegerField(_("Duration"), choices=CONTRACT_DURATION, default=THREE_DAYS)    
    contract_type = models.CharField(_('Contract Type'), choices=TYPES, default=INTERNAL, max_length=20)
    reaction = models.CharField(_('State'), choices=STATE, default=AWAITING, max_length=30)
    notes = models.TextField(null=True, blank=True, max_length=250)
    
    reference = models.CharField(_('Reference'), unique=True, blank=True, max_length=100)
    slug = models.SlugField(_('Slug'), max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    line_one = models.CharField(_('Service Description'), max_length=120, help_text=_("Enter your main product or service here"))
    line_one_quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    line_one_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0)
    line_one_total_price = models.PositiveIntegerField(_('Total'), default=0)
    
    line_one = models.CharField(_('Service Description'), max_length=120, help_text=_("Enter your main product or service here"))
    line_one_quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    line_one_unit_price = models.PositiveIntegerField(_('Unit Price'), default=0)
    line_one_total_price = models.PositiveIntegerField(_('Total'), default=0)

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
        return self.line_one

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("Contract")
        verbose_name_plural = _("Contract")

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_unique_reference()

        self.slug=(slugify(self.line_one))
 
        super(Contract, self).save(*args, **kwargs)


    def generate_unique_reference(self):
        max_attempts = 1000
        attempts = 0

        while attempts < max_attempts:
            # Generate a random UUID and convert it to a human-readable string
            # We set max_attempt to prevent function from going into potential infinite loop
            reference = str(uuid.uuid4()).replace('-', '')[:8].upper()

            # Check if the generated reference is unique
            if not Contract.objects.filter(reference=reference).exists():
                return reference

            attempts += 1

        raise ValueError("Failed to create transaction")


    def get_contract_detail_absolute_url(self):
        return reverse('contract:contract_single', args=[self.id])

    def get_redeem_contract_absolute_url(self):
        return reverse('contract:redeem_contract', args=[self.id])

    def get_internal_contract_detail_absolute_url(self):
        return reverse('contract:internal_contract_detail', args=[self.pk])

    def get_redeem_internal_contract_absolute_url(self):
        return reverse('contract:internal_contract_fee_structure', args=[self.slug])


    @classmethod
    def capture(cls, pk:int, reaction):
        contract = cls.objects.filter(pk=pk).first()
        if contract and contract.reaction != 'awaiting':
            raise ContractException('Contract must be in awaiting state to accept or reject')
        
        contract.reaction = reaction
        contract.save()

        return contract
        

class ContractChat(models.Model):
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="contractteamchat", on_delete=models.PROTECT)
    contract = models.ForeignKey(Contract, verbose_name=_("External Client"), related_name="contractclientchat", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='contractchatsender', on_delete=models.PROTECT)    
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message sent by {self.sender.get_full_name()}'

    class Meta:
        ordering = ['sent_on']
        verbose_name = _("Contract Chat")
        verbose_name_plural = _("Contract Chat")
























