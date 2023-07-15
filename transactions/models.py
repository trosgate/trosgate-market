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
from resolution.models import ProposalResolution, ProjectResolution, ContractResolution, ExtContractResolution
from merchants.models import MerchantMaster
from applications.models import Application


class PurchaseMaster(MerchantMaster):
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (SUCCESS, _('Success')),
        (FAILED, _('Failed'))
    )

    PROPOSAL = 'proposal'
    PROJECT = 'project'
    CONTRACT = 'contract'
    EX_CONTRACT = 'excontract'
    PURCHASE_CATEGORY = (
        (PROPOSAL, _('Proposal')),
        (PROJECT, _('Project')),
        (CONTRACT, _('Contract')),
        (EX_CONTRACT, _('Ex-Contract'))
    ) 
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary_paid = models.PositiveIntegerField(_("Salary Paid"))
    payment_method = models.CharField(_("Payment Method"), max_length=200, blank=True)
    category = models.CharField(_("Purchase Category"), max_length=20, choices=PURCHASE_CATEGORY, default='')    
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default=FAILED)    
    unique_reference = models.CharField(_("Unique Reference"), max_length=100, blank=True)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)

    class Meta:
        abstract = True


class Purchase(PurchaseMaster):
    client_fee = models.PositiveIntegerField(_("Client Fee"), default=0)
    paypal_order_key = models.CharField(_("PayPal Order Key"), max_length=200, null=True, blank=True)
    flutterwave_order_key = models.CharField(_("Flutterwave Order Key"), max_length=200, null=True, blank=True)
    stripe_order_key = models.CharField(_("Stripe Order Key"), max_length=200, null=True, blank=True)
    razorpay_order_key = models.CharField(_("Razorpay Order Key"), max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(_("Razorpay Payment ID"), max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(_("Razorpay Signature"), max_length=200, null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.payment_method} purchase made by {self.client.get_full_name()}'


    @classmethod
    def one_click_proposal(cls, user, proposal):
        with db_transaction.atomic():
            account = ClientAccount.objects.select_for_update().get(user=user)
            if account.available_balance < proposal.salary:
                raise FundException('Insufficuent Balance')

            earning_fee = get_proposal_fee_calculator(proposal.salary)
            total_earning = int(proposal.salary) - int(earning_fee)
            
            sales = cls.objects.create(
                client=account.user,
                payment_method='balance',
                client_fee = int(earning_fee),
                category = Purchase.PROPOSAL,
                salary_paid=proposal.salary,
                status = cls.SUCCESS,
            )
            stan = f'{sales.pk}'.zfill(8)
            sales.unique_reference = f'1click{sales.client.id}{stan}'
            sales.status=Purchase.SUCCESS
            sales.save()

            purchass = ProposalSale.objects.create(
                team = proposal.team,
                purchase=sales,  
                proposal=proposal, 
                sales_price=int(proposal.salary),
                earning_fee_charged=earning_fee,
                total_earning_fee_charged=earning_fee,
                disc_sales_price=int(proposal.salary),
                total_sales_price=int(proposal.salary),
                earning=total_earning,
                total_earning=total_earning
            )           
            
            ClientAccount.debit_available_balance(user=sales.client, available_balance=sales.salary_paid)

            FreelancerAccount.credit_pending_balance(user=purchass.team.created_by, pending_balance=sales.salary_paid, purchase=purchass)
        
        return account, sales, purchass


    @classmethod
    def one_click_intern_contract(cls, user, contract):
        with db_transaction.atomic():
            account = ClientAccount.objects.select_for_update().get(user=user)
                        
            if account.available_balance < contract.grand_total:
                raise FundException('Insufficient Balance')

            if contract is None:
                raise FundException('Contract not found')
            
            earning_fee = get_contract_fee_calculator(contract.grand_total)
            total_earning = int(contract.grand_total) - int(earning_fee)

            sales = cls.objects.create(
                client=account.user,
                payment_method='balance',
                client_fee = int(earning_fee),
                category = Purchase.CONTRACT,
                salary_paid=contract.grand_total,
                status = cls.SUCCESS,
            )
            stan = f'{sales.pk}'.zfill(8)
            sales.unique_reference = f'1click{sales.client.id}{stan}'
            sales.status=Purchase.SUCCESS
            sales.save()

            purchass = ContractSale.objects.create(
                team = contract.team,
                contract = contract,
                purchase=sales,
                sales_price=int(contract.grand_total),
                earning_fee_charged=earning_fee,
                total_earning_fee_charged=earning_fee,
                disc_sales_price=int(contract.grand_total),
                total_sales_price=int(contract.grand_total),
                earning=total_earning,
                total_earning=total_earning
            )   

            ClientAccount.debit_available_balance(user=sales.client, available_balance=sales.salary_paid)

            selected_contract = InternalContract.objects.select_for_update().get(pk=purchass.contract.id)
            selected_contract.reaction = 'paid'
            selected_contract.save()
            
            FreelancerAccount.credit_pending_balance(user=purchass.team.created_by, pending_balance=purchass.total_earning, purchase=selected_contract)

        return account, purchass, selected_contract


    @classmethod
    def one_click_extern_contract(cls, user, contract):
        with db_transaction.atomic():
            account = ClientAccount.objects.select_for_update().get(user=user)

            if account.available_balance < contract.grand_total:
                raise FundException('Insufficient Balance')
            
            if contract is None:    
                raise FundException('Contract error occured. Try again')

            if not contract:
                raise FundException('Contract not found')

            if contract is None:
                raise FundException('Contract error')
                            
            sales = cls.objects.create(
                client=account.user,
                payment_method='balance',
                category = Purchase.EX_CONTRACT,
                salary_paid=contract.grand_total,
                status = cls.SUCCESS,
            )
            stan = f'{sales.pk}'.zfill(8)
            sales.unique_reference = f'1click{sales.client.id}{stan}'
            sales.status=Purchase.SUCCESS
            sales.save()

            purchass = ExtContract.objects.create(
                team = contract.team,
                contract = contract,
                purchase=sales,
                sales_price=int(contract.grand_total),
                disc_sales_price=int(contract.grand_total),
                total_sales_price=int(contract.grand_total),
                earning=int(contract.grand_total),
                total_earning=int(contract.grand_total)
            )  

            ClientAccount.debit_available_balance(user=sales.client, available_balance=sales.salary_paid)

            selected_contract = Contract.objects.select_for_update().get(pk=purchass.contract.id)
            selected_contract.reaction = 'paid'
            selected_contract.save()
            
            FreelancerAccount.credit_pending_balance(user=purchass.team.created_by, pending_balance=purchass.total_earning, purchase=selected_contract)

        return account, purchass, selected_contract


    @classmethod
    def stripe_order_confirmation(cls, stripe_order_key):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(stripe_order_key=stripe_order_key)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded"))
            purchase.status = Purchase.SUCCESS
            purchase.save()

            contract = None
            contract_item = None
            
            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase, purchase__status='success'):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.proposal)
                    
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase, purchase__status='success'):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.project)
                    project = item.project
                    # applications = Application.objects.filter(project=project)) change the statuses
                    print(project)
                    # print(applications)

            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])
            
            if purchase.category == Purchase.EX_CONTRACT:
                contract_item = ExtContract.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = Contract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.line_one)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])

        return purchase, contract_item, contract


    @classmethod
    def paypal_order_confirmation(cls, pk):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(pk=pk)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded"))
            purchase.status = Purchase.SUCCESS
            purchase.save()

            contract = None
            contract_item = None

            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase, purchase__status='success'):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.proposal)
            
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase, purchase__status='success'):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.project)
            
            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])

            if purchase.category == Purchase.EX_CONTRACT:
                contract_item = ExtContract.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = Contract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.line_one)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])
                
        return purchase, contract_item, contract


    @classmethod
    def flutterwave_order_confirmation(cls, unique_reference, flutterwave_order_key):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(unique_reference=unique_reference)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded"))

            purchase.status = Purchase.SUCCESS
            purchase.flutterwave_order_key = flutterwave_order_key
            purchase.save()

            contract = None
            contract_item = None

            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.proposal)
            
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.project)
            
            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])

            if purchase.category == Purchase.EX_CONTRACT:
                contract_item = ExtContract.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = Contract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.line_one)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])

        return purchase, contract_item, contract
        

    @classmethod
    def razorpay_order_confirmation(cls, razorpay_order_key, razorpay_payment_id, razorpay_signature):
        with db_transaction.atomic():
            purchase = cls.objects.select_for_update().get(razorpay_order_key=razorpay_order_key)
            if purchase.status != Purchase.FAILED:
                raise Exception(_("This purchase already succeeded"))

            purchase.status = Purchase.SUCCESS
            purchase.razorpay_payment_id = razorpay_payment_id
            purchase.razorpay_signature = razorpay_signature
            purchase.save()

            contract = None
            contract_item = None

            if purchase.category == Purchase.PROPOSAL:
                for item in ProposalSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.proposal)
            
            if purchase.category == Purchase.PROJECT:
                for item in ApplicationSale.objects.filter(purchase=purchase):
                    FreelancerAccount.credit_pending_balance(user=item.team.created_by, pending_balance=item.total_sales_price, purchase=item.project)
            
            if purchase.category == Purchase.CONTRACT:
                contract_item = ContractSale.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = InternalContract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.proposal)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])

            if purchase.category == Purchase.EX_CONTRACT:
                contract_item = ExtContract.objects.select_for_update().get(purchase=purchase, purchase__status='success')
                contract = Contract.objects.select_for_update().get(pk=contract_item.contract.id)
                FreelancerAccount.credit_pending_balance(user=contract_item.team.created_by, pending_balance=contract_item.total_sales_price, purchase=contract_item.contract.line_one)
                contract.reaction = 'paid'
                contract.save()
                # contract.save(update_fields=['reaction'])

        return purchase, contract_item, contract


class MerchantTransaction(MerchantMaster):
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name=_("Purchase Client"), on_delete=models.CASCADE)
    sales_price = models.PositiveIntegerField(_("Sales Price"), default=0)
    total_sales_price = models.PositiveIntegerField(_("Applicant Budget"), default=0)
    disc_sales_price = models.PositiveIntegerField(_("Discounted Salary"), default=0)
    staff_hired = models.PositiveIntegerField(_("Staff Hired"), default=1)
    earning_fee_charged = models.PositiveIntegerField(_("Earning Fee"), default=0)
    total_earning_fee_charged = models.PositiveIntegerField(_("Total Earning Fee"), default=0)
    discount_offered = models.PositiveIntegerField(_("Discount Offered"), default=0)
    total_discount_offered = models.PositiveIntegerField(_("Total Discount"), default=0)
    earning = models.PositiveIntegerField(_("Earning"), default=0)
    total_earning = models.PositiveIntegerField(_("Total Earning"), default=0)
    created_at = models.DateTimeField(_("Ordered On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified On"), auto_now=True)
    is_refunded = models.BooleanField(_("Refunded"), default=False)

    class Meta:
        abstract = True


class ProposalSale(MerchantTransaction):
    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'
    PRICING_TIERS = (
        (BASIC, _("Basic")),
        (STANDARD, _("Standard")),
        (PREMIUM, _("Premium")),
    )    
    proposal = models.ForeignKey("proposals.Proposal", verbose_name=_("Proposal Hired"), related_name="proposalhired", on_delete=models.CASCADE)
    revision = models.PositiveIntegerField(_("Revision"))
    duration = models.PositiveIntegerField(_("Duration"))
    package_name = models.CharField(_("Selected Package"), max_length=20)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):

        if self.proposal.pricing:
            pricing_tier_revisions = {
                Proposal.BASIC: self.proposal.revision_tier1,
                Proposal.STANDARD: self.proposal.revision_tier2,
                Proposal.PREMIUM: self.proposal.revision_tier3,
            }
            pricing_tier_durations = {
                Proposal.BASIC: self.proposal.pricing1_duration,
                Proposal.STANDARD: self.proposal.pricing2_duration,
                Proposal.PREMIUM: self.proposal.pricing3_duration,
            }

            self.revision = pricing_tier_revisions.get(self.package_name)
            self.duration = pricing_tier_durations.get(self.package_name)
        else:
            self.revision = self.proposal.revision
            self.duration = self.proposal.duration
        super(ProposalSale, self).save(*args, **kwargs)


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

            # if proposal_sale.purchase.status != Purchase.SUCCESS:
            #     raise Exception(_("You cannot issue refund for a failed transaction"))

            if resolution.status == ProposalResolution.COMPLETED:
                raise Exception(_("This transaction was completed and closed so cannot be refunded"))

            resolution.status = ProposalResolution.CANCELLED
            resolution.save()

            proposal_sale.is_refunded = True
            proposal_sale.save()
            
            freelancer.pending_balance -= int(proposal_sale.total_sales_price)
            freelancer.save(update_fields=['pending_balance'])

            client.available_balance += int(proposal_sale.total_sales_price)
            client.save(update_fields=['available_balance'])
            
        return proposal_sale, client, freelancer, resolution


class ContractSale(MerchantTransaction):
    contract = models.ForeignKey("contract.InternalContract", verbose_name=_("Contract Hired"), related_name="contracthired", on_delete=models.CASCADE)

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

            # if contract_sale.purchase.status != Purchase.SUCCESS:
            #     raise Exception(_("You cannot issue refund for a failed transaction"))

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


class ExtContract(MerchantTransaction):
    # status choices to be added to track the state of order
    contract = models.ForeignKey("contract.Contract", verbose_name=_("Contract Hired"), related_name="extcontracthired", on_delete=models.CASCADE)

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
                resolution = ExtContractResolution.objects.select_for_update().get(contract_sale=contract_sale)            
            except:
                raise Exception(_("Sorry! refund cannot be raised for this transaction. It could be that Team is yet to start work"))
            
            if contract_sale.is_refunded != False:
                raise Exception(_("This transaction cannot be refunded twice"))

            # if contract_sale.purchase.status != Purchase.SUCCESS:
            #     raise Exception(_("You cannot issue refund for a failed transaction"))

            if resolution.status == ProjectResolution.COMPLETED:
                raise Exception(_("This transaction was completed and closed so cannot be refunded"))

            resolution.status = ProjectResolution.CANCELLED
            resolution.save()

            contract_sale.is_refunded = True
            contract_sale.save()
            
            freelancer.pending_balance -= int(contract_sale.total_sales_price)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(contract_sale.total_sales_price)
            client.save(update_fields=['available_balance'])

        return contract_sale, client, freelancer, resolution


class ApplicationSale(MerchantTransaction):
    project = models.ForeignKey("projects.Project", verbose_name=_("Project Applied"), related_name="applicantprojectapplied", on_delete=models.CASCADE)

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
                raise Exception(_("Sorry! could not raise refund. It could be that Team is yet to start work"))
            
            if application.is_refunded != False:
                raise Exception(_("This transaction cannot be refunded twice"))

            # if application.purchase.status != Purchase.SUCCESS:
            #     raise Exception(_("You cannot issue refund for a failed transaction"))

            if resolution.status == ProjectResolution.COMPLETED:
                raise Exception(_("This transaction was completed and closed so cannot be refunded"))

            resolution.status = ProjectResolution.CANCELLED
            resolution.save()

            application.is_refunded = True
            application.save()
            
            freelancer.pending_balance -= int(application.total_sales_price)
            freelancer.save(update_fields=['pending_balance'])
            
            client.available_balance += int(application.total_sales_price)
            client.save(update_fields=['available_balance'])

        return application, client, freelancer, resolution


class SubscriptionMaster(MerchantMaster):
    payment_method = models.CharField(_("Payment Method"), max_length=200, blank=True)
    price = models.PositiveIntegerField()
    status = models.BooleanField(_("Paid"), choices=((False, 'No'), (True, 'Yes')), default=False)
    customer_id = models.CharField(_("Customer ID"), max_length=255, blank=True, null=True)
    subscription_id = models.CharField(_("Subscription ID"), max_length=255, blank=True, null=True)    
    created_at = models.DateTimeField(_("Subscription Start"), blank=True, null=True)
    activation_time = models.DateTimeField(_("Activation Time"), blank=True, null=True)
    expired_time = models.DateTimeField(_("Est. Expiration"), blank=True, null=True)

    class Meta:
        abstract = True


class Plan(SubscriptionMaster):

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        
    def __str__(self):
        return str(self.team.title)


class SubscriptionItem(SubscriptionMaster):
    team = models.ForeignKey("teams.Team", verbose_name=_("Team"), related_name='subscriptionteam', on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        
    def __str__(self):
        return str(self.team.title)
