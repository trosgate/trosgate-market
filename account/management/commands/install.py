from django.core.management.base import BaseCommand
from django.core.management import call_command
from account.models import Country, Package, Customer, Merchant
from general_settings . models import (
    WebsiteSetting, Category, Department, Size, PaymentsControl, 
    SubscriptionGateway, DepositControl, ProposalGuides, Mailer,
    Skill, DiscountSystem, DepositGateway, HiringFee, 
    Currency, Payday, StorageBuckets, TestEmail, 
    AutoLogoutSystem, ExachangeRateAPI
)
from payments.models import PaymentGateway
from control_settings.models import LayoutSetting
from teams . models import Team, Invitation
from proposals . models import Proposal
from projects.models import Project
from analytics.models import NewStats
from marketing.models import AutoTyPist
from pages.models import TermsAndConditions, Hiring, Freelancing, AboutUsPage
from freelancer.models import Freelancer
from client.models import Client

# New scripts
from transactions.models import (
    OneClickPurchase, Purchase, ApplicationSale, ProposalSale, 
    ContractSale,ExtContract, SubscriptionItem
)
from resolution.models import (
    OneClickResolution, ProposalResolution, ProjectResolution, 
    ContractResolution, ExtContractResolution
) 


class Command(BaseCommand):
    help = "this creates default values via commands for the entire system"

    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        
        # INITIAL DATABASE POPULATOR STARTS

        if not Package.objects.count():
            call_command("loaddata", "fixures/db_packages.json")

        if not Country.objects.count():
            call_command("loaddata", "fixures/db_countries.json")

        if not NewStats.objects.count():
            call_command("loaddata", "fixures/db_statistics.json")

        if not AutoTyPist.objects.count():
            call_command("loaddata", "fixures/db_autotypist.json")

        # Customer.objects.all().exclude(pk=2).delete()
        # if not Customer.objects.count():
        #     call_command("loaddata", "fixures/db_admin_auth.json")

        # if not Merchant.objects.count():
        #     call_command("loaddata", "fixures/db_merchant.json")

        if not LayoutSetting.objects.count():
            call_command("loaddata", "fixures/db_layout.json")

        if not WebsiteSetting.objects.count():
            call_command("loaddata", "fixures/db_admin_settings.json")

        if not StorageBuckets.objects.count():
            call_command("loaddata", "fixures/db_storage.json")

        if not TestEmail.objects.count():
            call_command("loaddata", "fixures/db_testmail.json")

        # if not PaymentAPIs.objects.count():
        #     call_command("loaddata", "fixures/db_paymentapis.json")

        if not AutoLogoutSystem.objects.count():
            call_command("loaddata", "fixures/db_autologout.json")

        if not PaymentGateway.objects.count():
            call_command("loaddata", "fixures/db_payment_gateways.json")

        if not SubscriptionGateway.objects.count():
            call_command("loaddata", "fixures/db_subscriptionplan.json")

        if not DepositGateway.objects.count():
            call_command("loaddata", "fixures/db_deposit.json")

        if not Category.objects.count():
            call_command("loaddata", "fixures/db_categories.json")

        if not Skill.objects.count():
            call_command("loaddata", "fixures/db_skills.json")

        if not Size.objects.count():
            call_command("loaddata", "fixures/db_business_size.json")

        if not Department.objects.count():
            call_command("loaddata", "fixures/db_department.json")
        
        if not ProposalGuides.objects.count():
            call_command("loaddata", "fixures/db_instructions.json")

        if not DiscountSystem.objects.count():
            call_command("loaddata", "fixures/db_discount_system.json")

        if not HiringFee.objects.count():
            call_command("loaddata", "fixures/db_freelancer_fee.json")

        if not Currency.objects.count():
            call_command("loaddata", "fixures/db_currencies.json")
        
        if not ExachangeRateAPI.objects.count():
            call_command("loaddata", "fixures/db_currexchangerate.json")

        if not PaymentsControl.objects.count():
            call_command("loaddata", "fixures/db_fund_control.json")

        if not DepositControl.objects.count():
            call_command("loaddata", "fixures/db_deposit_control.json")

        if not Payday.objects.count():
            call_command("loaddata", "fixures/db_payday.json")

        if not Mailer.objects.count():
            call_command("loaddata", "fixures/db_mailer.json")

        if not Hiring.objects.count():
            call_command("loaddata", "fixures/db_howitworkhiring.json")
        
        if not Freelancing.objects.count():
            call_command("loaddata", "fixures/db_howitworkfreelancing.json")

        if not AboutUsPage.objects.count():
            call_command("loaddata", "fixures/db_aboutus.json")

        if not TermsAndConditions.objects.count():
            call_command("loaddata", "fixures/db_termsandcond.json")
        
        
        # INITIAL DATABASE POPULATOR ENDS

        # FIXURE OBJECTS INSERTION STARTS FROM HERE

        # if not Freelancer.objects.count():
        #     call_command("loaddata", "fixures/db_freelancer_auth.json")

        # customers = Customer.objects.filter(user_type='freelancer')
        # teams = Team.objects.all()
        # for customer, team in zip(customers, teams):
        #     Invitation.objects.create(
        #         team = team, 
        #         sender = customer, 
        #         email = customer.email, 
        #         type = 'founder',
        #         status = 'accepted'
        #     )


        # if not Project.objects.count():
        #     call_command("loaddata", "db_projects.json")

        # if not Proposal.objects.count():
        #     call_command("loaddata", "db_proposals.json")

        # if not OneClickPurchase.objects.count():
        #     call_command("loaddata", "db_oneclickpurchase.json")

        # if not Purchase.objects.count():
        #     call_command("loaddata", "db_purchase.json")

        # if not ApplicationSale.objects.count():
        #     call_command("loaddata", "db_applicationsale.json")

        # if not ProposalSale.objects.count():
        #     call_command("loaddata", "db_proposalsale.json")

        # if not ContractSale.objects.count():
        #     call_command("loaddata", "db_contractsale.json")

        # if not ExtContract.objects.count():
        #     call_command("loaddata", "db_extcontractsale.json")

        # if not SubscriptionItem.objects.count():
        #     call_command("loaddata", "db_subscription.json")
        
        # if not OneClickResolution.objects.count():
        #     call_command("loaddata", "db_oneclickresolver.json")

        # if not ProjectResolution.objects.count():
        #     call_command("loaddata", "db_projectresolver.json")
            
        # if not ProposalResolution.objects.count():
        #     call_command("loaddata", "db_proposalresolver.json")
            
        # if not ContractResolution.objects.count():
        #     call_command("loaddata", "db_contractresolver.json")
            
        # FIXURE OBJECT INSERTION ENDS
