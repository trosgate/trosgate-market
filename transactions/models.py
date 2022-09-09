import uuid
import secrets
from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.safestring import mark_safe
from django.urls import reverse
from freelancer.models import FreelancerAccount
from proposals.models import Proposal
from django.conf import settings
from django.core.exceptions import ValidationError
from general_settings.currency import get_base_currency_symbol
from contract.models import InternalContract, Contract
from client.models import ClientAccount
from general_settings.fees_and_charges import get_contract_fee_calculator, get_proposal_fee_calculator, get_external_contract_fee_calculator
from account.fund_exception import FundException
from teams.models import Team
from client.models import ClientAccount
from resolution.models import ProposalResolution, ProjectResolution, ContractResolution


class OneClickPurchase(models.Model):
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (SUCCESS, _('Success')),
        (FAILED, _('Failed'))
    )    

    PROPOSAL = 'proposal'
    CONTRACT = 'contract'
    EXTERNAL_CONTRACT = 'externalcontract'
    PURCHASE_CATEGORY = (
        (PROPOSAL, _('Proposal')),
        (CONTRACT, _('Contract')),
        (EXTERNAL_CONTRACT, _('External Contract'))
    )    
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="oneclickclient")
    salary_paid = models.PositiveIntegerField(_("Salary Paid"))
    total_earning = models.PositiveIntegerField(_("Totoal Earning"))
    earning_fee = models.PositiveIntegerField(_("Earning Fee"))
    payment_method = models.CharField(_("Payment Method"), max_length=200, blank=True)
    category = models.CharField(_("Purchase Category"), max_length=20, choices=PURCHASE_CATEGORY, default='')    
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default=FAILED)    
    reference = models.CharField(_("Reference"), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)
    
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='oneclickteam', on_delete=models.PROTECT)
    proposal = models.ForeignKey("proposals.Proposal", verbose_name=_("Proposal"), related_name="oneclickproposal", null=True, blank=True, on_delete=models.PROTECT)
    contract = models.ForeignKey("contract.InternalContract", verbose_name=_("Int Contract"), related_name="intoneclickcontract", null=True, blank=True, on_delete=models.PROTECT)
    extcontract = models.ForeignKey("contract.Contract", verbose_name=_("Ext Contract"), related_name="extoneclickcontract", null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("One Click Purchase")
        verbose_name = ("One Click Purchase")

    def __str__(self):
        return f'1-Click Purchase - {self.reference}'


    @classmethod
    def one_click_proposal(cls, user, proposal):
        with db_transaction.atomic():
            account = ClientAccount.objects.select_for_update().get(user = user)
            if account.available_balance < proposal.salary:
                raise FundException('Insufficuent Balance')

            earning_fee = get_proposal_fee_calculator(proposal.salary)
            total_earning = int(proposal.salary) - int(earning_fee)
            
            purchass = cls.objects.create(
                client=account.user,
                category = cls.PROPOSAL,
                payment_method='Balance',
                salary_paid=proposal.salary,
                total_earning=round(total_earning),
                earning_fee=earning_fee,
                team = proposal.team,
                proposal = proposal,
                status = cls.SUCCESS,
            )           
            stan = f'{purchass.pk}'.zfill(8)
            purchass.reference = f'1click{purchass.client.id}{stan}'
            purchass.save()

            ClientAccount.debit_available_balance(user=purchass.client, available_balance=purchass.salary_paid)

            FreelancerAccount.credit_pending_balance(user=purchass.team.created_by, pending_balance=purchass.total_earning, paid_amount=purchass.salary_paid, purchase=purchass.proposal)
        
        return account, purchass


    @classmethod
    def one_click_intern_contract(cls, user, contract):
        with db_transaction.atomic():
            account = ClientAccount.objects.select_for_update().get(user=user)
            if account.available_balance < contract.grand_total:
                raise FundException('Insufficient Balance')

            earning_fee = get_contract_fee_calculator(contract.grand_total)
            total_earning = int(contract.grand_total) - int(earning_fee)
            
            if not contract:
                raise FundException('Contract not found')

            if contract is None:
                raise FundException('Contract error')

            purchass = cls.objects.create(
                client=account.user,
                category = cls.CONTRACT,
                payment_method='Balance',
                salary_paid=contract.grand_total,
                total_earning=round(total_earning),
                earning_fee=earning_fee,
                team = contract.team,
                contract = contract,
                status = cls.SUCCESS,
            )           
            stan = f'{purchass.pk}'.zfill(8)
            purchass.reference = f'1click{purchass.client.id}{stan}'
            purchass.save()

            ClientAccount.debit_available_balance(user=purchass.client, available_balance=purchass.salary_paid)

            selected_contract = InternalContract.objects.select_for_update().get(pk=purchass.contract.id)
            selected_contract.reaction = 'paid'
            selected_contract.save(update_fields=['reaction'])
            
            FreelancerAccount.credit_pending_balance(user=purchass.team.created_by, pending_balance=purchass.total_earning, paid_amount=purchass.salary_paid, purchase=selected_contract)

        return account, purchass, selected_contract


    @classmethod
    def one_click_extern_contract(cls, user, contract):
        with db_transaction.atomic():
            account = ClientAccount.objects.select_for_update().get(user=user)

            if contract is None:    
                raise FundException('Contract error occured. Try again')

            if account.available_balance < contract.grand_total:
                raise FundException('Insufficient Balance')

            earning_fee = get_external_contract_fee_calculator(contract.grand_total)
            total_earning = int(contract.grand_total) - int(earning_fee)

            if not contract:
                raise FundException('Contract not found')

            if contract is None:
                raise FundException('Contract error')
                            
            purchass = cls.objects.create(
                client=account.user,
                category = cls.EXTERNAL_CONTRACT,
                payment_method='Balance',
                salary_paid=contract.grand_total,
                total_earning=round(total_earning),
                earning_fee=earning_fee,
                team = contract.team,
                extcontract = contract,
                status = cls.SUCCESS,                
            )           
            stan = f'{purchass.pk}'.zfill(8)
            purchass.reference = f'1click{purchass.client.id}{stan}'
            purchass.save()

            ClientAccount.debit_available_balance(user=purchass.client, available_balance=purchass.salary_paid)

            selected_contract = Contract.objects.select_for_update().get(pk=purchass.extcontract.id)
            selected_contract.reaction = 'paid'
            selected_contract.save(update_fields=['reaction'])
            
            FreelancerAccount.credit_pending_balance(user=purchass.team.created_by, pending_balance=purchass.total_earning, paid_amount=purchass.salary_paid, purchase=selected_contract)

        return account, purchass, selected_contract


class Purchase(models.Model):
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (SUCCESS, _('Success')),
        (FAILED, _('Failed'))
    )    

    ONE_CLICK = 'one_click'
    PROPOSAL = 'proposal'
    PROJECT = 'project'
    CONTRACT = 'contract'
    PURCHASE_CATEGORY = (
        (ONE_CLICK, _('One Click')),
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
    paypal_order_key = models.CharField(_("PayPal Order Key"), max_length=200, null=True, blank=True)
    flutterwave_order_key = models.CharField(_("Flutterwave Order Key"), max_length=200, null=True, blank=True)
    stripe_order_key = models.CharField(_("Stripe Order Key"), max_length=200, null=True, blank=True)
    razorpay_order_key = models.CharField(_("Razorpay Order Key"), max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(_("Razorpay Payment ID"), max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(_("Razorpay Signature"), max_length=200, null=True, blank=True)
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
    is_refunded = models.BooleanField(_("Refunded"), default=False)

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

    @classmethod
    def application_refund(cls, pk:int):
        with db_transaction.atomic():
            application = cls.objects.select_for_update().get(pk=pk)
            client = ClientAccount.objects.select_for_update().get(user=application.purchase.client)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=application.team.created_by)
            
            try:
                resolution = ProjectResolution.objects.select_for_update().get(application=application)            
            except:
                raise Exception(_("Sorry! refund cannot be raised for this transaction. It could be that Team is yet to start work"))
            
            if application.is_refunded != False:
                raise Exception(_("This transaction cannot be refunded twice"))

            if application.purchase.status != Purchase.SUCCESS:
                raise Exception(_("You cannot issue refund for a failed transaction"))

            if resolution.status == ProjectResolution.COMPLETED:
                raise Exception(_("This transaction was completed and closed so cannot be refunded"))

            resolution.status = ProjectResolution.CANCELLED
            resolution.save()

            application.is_refunded = True
            application.save()
            
            freelancer.pending_balance -= int(application.total_earnings)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(application.total_sales_price)
            client.save(update_fields=['available_balance'])

        return application, client, freelancer, resolution


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
    is_refunded = models.BooleanField(_("Refunded"), default=False)

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

    @classmethod
    def proposal_refund(cls, pk:int):
        with db_transaction.atomic():
            proposal_sale = cls.objects.select_for_update().get(pk=pk)
            client = ClientAccount.objects.select_for_update().get(user=proposal_sale.purchase.client)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=proposal_sale.team.created_by)
            
            try:
                resolution = ProposalResolution.objects.select_for_update().get(proposal_sale=proposal_sale)            
            except:
                raise Exception(_("Sorry! refund cannot be raised for this transaction. It could be that Team is yet to start work"))
            
            if proposal_sale.is_refunded != False:
                raise Exception(_("This transaction cannot be refunded twice"))

            if proposal_sale.purchase.status != Purchase.SUCCESS:
                raise Exception(_("You cannot issue refund for a failed transaction"))

            if resolution.status == ProposalResolution.COMPLETED:
                raise Exception(_("This transaction was completed and closed so cannot be refunded"))

            resolution.status = ProposalResolution.CANCELLED
            resolution.save()

            proposal_sale.is_refunded = True
            proposal_sale.save()
            
            freelancer.pending_balance -= int(proposal_sale.total_earning)
            freelancer.save(update_fields=['pending_balance'])

            client.available_balance += int(proposal_sale.total_sales_price)
            client.save(update_fields=['available_balance'])
            
        return proposal_sale, client, freelancer, resolution


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
    is_refunded = models.BooleanField(_("Refunded"), default=False)

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

    @classmethod
    def contract_refund(cls, pk:int):
        with db_transaction.atomic():
            contract_sale = cls.objects.select_for_update().get(pk=pk)
            client = ClientAccount.objects.select_for_update().get(user=contract_sale.purchase.client)
            freelancer = FreelancerAccount.objects.select_for_update().get(user=contract_sale.team.created_by)
            
            try:
                resolution = ContractResolution.objects.select_for_update().get(contract_sale=contract_sale)            
            except:
                raise Exception(_("Sorry! refund cannot be raised for this transaction. It could be that Team is yet to start work"))
            
            if contract_sale.is_refunded != False:
                raise Exception(_("This transaction cannot be refunded twice"))

            if contract_sale.purchase.status != Purchase.SUCCESS:
                raise Exception(_("You cannot issue refund for a failed transaction"))

            if resolution.status == ProjectResolution.COMPLETED:
                raise Exception(_("This transaction was completed and closed so cannot be refunded"))

            resolution.status = ProjectResolution.CANCELLED
            resolution.save()

            contract_sale.is_refunded = True
            contract_sale.save()
            
            freelancer.pending_balance -= int(contract_sale.total_earning)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(contract_sale.total_sales_price)
            client.save(update_fields=['available_balance'])

        return contract_sale, client, freelancer, resolution


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
