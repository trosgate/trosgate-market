from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
import uuid
import secrets
from django.utils.safestring import mark_safe
from django.urls import reverse
from proposals.models import Proposal
from django.conf import settings
from django.core.exceptions import ValidationError
from general_settings.currency import get_base_currency_symbol


class Purchase(models.Model):
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (SUCCESS, _('Success')),
        (FAILED, _('Failed'))
    )    
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orderclient")
    full_name = models.CharField(_("Full Name"), max_length=100)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    phone = models.CharField(_("Phone Number"), max_length=100, null=True, blank=True)
    country = models.CharField(_("Country"), max_length=150, blank=True)
    salary_paid = models.PositiveIntegerField(_("Salary Paid"))
    payment_method = models.CharField(_("Payment Method"), max_length=200, blank=True)   
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
        return str(self.client.short_name)


class ApplicationSale(models.Model):
    #status choices to be added to track the state of order
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='hiredapplicantteam', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchase Client"), related_name="applicantionsales", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Applied"), related_name="applicantprojectapplied", on_delete=models.CASCADE)
    sales_price = models.PositiveIntegerField(_("Sales Price"))
    total_sales_price = models.PositiveIntegerField(_("Applicant Budget"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"))
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    Total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earnings = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

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
    total_sales_price = models.PositiveIntegerField(_("Proposal Salary"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"))
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    Total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earning = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

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
    #status choices to be added to track the state of order
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='hiredcontractteam', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchase Client"), related_name="contractsales", on_delete=models.CASCADE)
    contract = models.ForeignKey("contract.InternalContract", verbose_name=_("Contract Hired"), related_name="contracthired", on_delete=models.CASCADE)
    sales_price = models.PositiveIntegerField(_("Sales Price"))
    total_sales_price = models.PositiveIntegerField(_("Contract Total"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"))
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    Total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earning = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

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


class SalesReporting(models.Model):
    #
    # Item Type
    PROJECT = 'project'
    CONTRACT = 'contract'
    PROPOSAL = 'proposal'
    PRODUCT_TYPE = (
        (PROJECT, _('Project')),
        (CONTRACT, _('Contract')),
        (PROPOSAL, _('Proposal'))
    )
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='earningteam', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchased Client"), related_name="totalpurchase", on_delete=models.CASCADE)
    sales_category = models.CharField(_("Sales Category"), max_length=50, blank=True)
    sales_price = models.PositiveIntegerField(_("Total Sales"))
    total_sales_price = models.PositiveIntegerField(_("Total Sales"), blank=True, null=True)
    staff_hired = models.PositiveIntegerField(_("Total Staff Hired"), default=1)
    client_fee_charged = models.PositiveIntegerField(_("Client Fee"))
    freelancer_fee_charged = models.PositiveIntegerField(_("Freelancer Fee"))
    total_freelancer_fee_charged = models.PositiveIntegerField(_("Total Freelancer Fee"), blank=True, null=True)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"))
    Total_discount_offered = models.PositiveIntegerField(_("Total Discount"), blank=True, null=True)
    earning = models.PositiveIntegerField(_("Earning"))
    total_earning = models.PositiveIntegerField(_("Total Earning"), blank=True, null=True)

    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Client"), related_name='created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.purchase.client.short_name)

    def status_value(self):
        return self.purchase.get_status_display()


class SubscriptionItem(models.Model):
    team = models.ForeignKey("teams.Team", verbose_name=_(
        "Team"), related_name='subscriptionteam', on_delete=models.CASCADE)
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teamsubscriber")
    payment_method = models.CharField(
        _("Payment Method"), max_length=200, blank=True)
    price = models.PositiveIntegerField()
    status = models.BooleanField(_("Paid"), choices=(
        (False, 'No'), (True, 'Yes')), default=False)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

    def __str__(self):
        return str(self.subscriber)
