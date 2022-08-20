import uuid
import secrets
from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.safestring import mark_safe
from django.urls import reverse
from freelancer.models import Freelancer
from proposals.models import Proposal
from django.conf import settings
from django.core.exceptions import ValidationError
from general_settings.currency import get_base_currency_symbol
from payments import signals
from freelancer.models import FreelancerAccount
from contract.models import InternalContract

class Purchase(models.Model):
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (SUCCESS, _('Success')),
        (FAILED, _('Failed'))
    )    

    PROPOSAL = 'proposal'
    PROJECT = 'project'
    CONTRACT = 'contract'
    PURCHASE_CATEGORY = (
        (PROPOSAL, _('Proposal')),
        (PROJECT, _('Project')),
        (CONTRACT, _('Contract'))
    )    
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orderclient")
    full_name = models.CharField(_("Full Name"), max_length=100)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    phone = models.CharField(_("Phone Number"), max_length=100, null=True, blank=True)
    country = models.CharField(_("Country"), max_length=150, blank=True)
    salary_paid = models.PositiveIntegerField(_("Salary Paid"))
    client_fee = models.PositiveIntegerField(_("Client Fee"))
    payment_method = models.CharField(_("Payment Method"), max_length=200, blank=True)
    category = models.CharField(_("Purchase Category"), max_length=20, choices=PURCHASE_CATEGORY, default='')    
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default=FAILED)    
    unique_reference = models.CharField(_("Unique Reference"), max_length=100, blank=True)
    paypal_order_key = models.CharField(_("PayPal Order Key"), max_length=200, blank=True)
    flutterwave_order_key = models.CharField(_("Flutterwave Order Key"), max_length=250, null=True, blank=True)
    stripe_order_key = models.CharField(_("Stripe Order Key"), max_length=250, null=True, blank=True)
    razorpay_order_key = models.CharField(_("Razorpay Order Key"), max_length=250, null=True, blank=True)
    razorpay_payment_id = models.CharField(_("Razorpay Payment ID"), max_length=250, null=True, blank=True)
    razorpay_signature = models.CharField(_("Razorpay Signature"), max_length=250, null=True, blank=True)

    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.payment_method} purchase made by {self.client.get_full_name()}'


    @classmethod
    def stripe_order_confirmation(cls, stripe_order_key):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(stripe_order_key=stripe_order_key)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded and cannot be processed"))
            purchase.status = Purchase.SUCCESS
            purchase.save()

            contract = ''
            contract_item = ''
            
            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_earning, paid_amount=item.total_sales_price, purchase=item.proposal)
            
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_earnings, paid_amount=item.total_sales_price, purchase=item.project)
            
            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_earning, paid_amount=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save(update_fields=['reaction'])

        return purchase, contract_item, contract


    @classmethod
    def paypal_order_confirmation(cls, pk):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(pk=pk)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded and cannot be processed"))
            purchase.status = Purchase.SUCCESS
            purchase.save()

            contract = ''
            contract_item = ''

            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_earning, paid_amount=item.total_sales_price, purchase=item.proposal)
            
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_earnings, paid_amount=item.total_sales_price, purchase=item.project)
            
            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_earning, paid_amount=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save(update_fields=['reaction'])

        return purchase, contract_item, contract


    @classmethod
    def razorpay_order_confirmation(cls, razorpay_order_key, razorpay_payment_id, razorpay_signature):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(razorpay_order_key=razorpay_order_key)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded and cannot be processed"))
            purchase.status = Purchase.SUCCESS
            purchase.razorpay_payment_id = razorpay_payment_id
            purchase.razorpay_signature = razorpay_signature
            purchase.save()

            contract = ''
            contract_item = ''

            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_earning, paid_amount=item.total_sales_price, purchase=item.proposal)
            
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_earnings, paid_amount=item.total_sales_price, purchase=item.project)
            
            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_earning, paid_amount=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save(update_fields=['reaction'])

        return purchase, contract_item, contract




class ApplicationSale(models.Model):
    #status choices to be added to track the state of order
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='hiredapplicantteam', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchase Client"), related_name="applicantionsales", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Applied"), related_name="applicantprojectapplied", on_delete=models.CASCADE)
    sales_price = models.PositiveIntegerField(_("Sales Price"))
    total_sales_price = models.PositiveIntegerField(_("Applicant Budget"), blank=True, null=True)
    disc_sales_price = models.PositiveIntegerField(_("Discounted Salary"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"))
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earnings = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.project) 

    def total_earning_fee(self):
        return f'{get_base_currency_symbol()} {self.earning_fee_charged}'

    def total_discount(self):
        return f'{get_base_currency_symbol()} {self.discount_offered}'

    def total_earning(self):
        return f'{get_base_currency_symbol()} {self.earning}'

    def status_value(self):
        return self.purchase.get_status_display()


class ProposalSale(models.Model):
    #status choices to be added to track the state of order
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='hiredproposalteam', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchase Client"), related_name="proposalsales", on_delete=models.CASCADE)
    proposal = models.ForeignKey("proposals.Proposal", verbose_name=_("Proposal Hired"), related_name="proposalhired", on_delete=models.CASCADE)
    sales_price = models.PositiveIntegerField(_("Sales Price"))
    total_sales_price = models.PositiveIntegerField(_("Total Salary"), blank=True, null=True)
    disc_sales_price = models.PositiveIntegerField(_("Discounted Salary"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"))
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earning = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.proposal)

    def earning_fee(self):
        return f'{get_base_currency_symbol()} {self.earning_fee_charged}'

    def total_earning_fee(self):
        return f'{get_base_currency_symbol()} {self.total_earning_fee_charged}'

    def total_discount(self):
        return f'{get_base_currency_symbol()} {self.discount_offered}'

    def total_discount(self):
        return f'{get_base_currency_symbol()} {self.Total_discount_offered}'

    def earnings(self):
        return f'{get_base_currency_symbol()} {self.earning}'

    def earnings(self):
        return f'{get_base_currency_symbol()} {self.total_earning}'

    def status_value(self):
        return self.purchase.get_status_display()


class ContractSale(models.Model):
    # status choices to be added to track the state of order
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='hiredcontractteam', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchase Client"), related_name="contractsales", on_delete=models.CASCADE)
    contract = models.ForeignKey("contract.InternalContract", verbose_name=_("Contract Hired"), related_name="contracthired", on_delete=models.CASCADE)
    sales_price = models.PositiveIntegerField(_("Sales Price"))
    total_sales_price = models.PositiveIntegerField(_("Contract Total"), blank=True, null=True)
    disc_sales_price = models.PositiveIntegerField(_("Discounted Salary"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"))
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earning = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.contract)

    def earning_fee(self):
        return f'{get_base_currency_symbol()} {self.earning_fee_charged}'

    def total_earning_fee(self):
        return f'{get_base_currency_symbol()} {self.total_earning_fee_charged}'

    def total_discount(self):
        return f'{get_base_currency_symbol()} {self.discount_offered}'

    def total_discount(self):
        return f'{get_base_currency_symbol()} {self.Total_discount_offered}'

    def earnings(self):
        return f'{get_base_currency_symbol()} {self.earning}'

    def earnings(self):
        return f'{get_base_currency_symbol()} {self.total_earning}'

    def status_value(self):
        return self.purchase.get_status_display()


class SubscriptionItem(models.Model):
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='subscriptionteam', on_delete=models.CASCADE)
    payment_method = models.CharField(_("Payment Method"), max_length=200, blank=True)
    price = models.PositiveIntegerField()
    status = models.BooleanField(_("Paid"), choices=((False, 'No'), (True, 'Yes')), default=False)
    customer_id = models.CharField(_("Customer ID"), max_length=255, blank=True, null=True)
    subscription_id = models.CharField(_("Subscription ID"), max_length=255, blank=True, null=True)    
    created_at = models.DateTimeField(_("Subscription Start"), blank=True, null=True)
    activation_time = models.DateTimeField(_("Activation Time"), blank=True, null=True)
    expired_time = models.DateTimeField(_("Est. Expiration"), blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        
    def __str__(self):
        return str(self.team.title)
