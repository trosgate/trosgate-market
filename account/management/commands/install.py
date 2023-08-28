from django.core.management.base import BaseCommand
from django.core.management import call_command
from general_settings . models import (
    WebsiteSetting, Category, Department, Size, PaymentsControl, 
    SubscriptionGateway, DepositControl, ProposalGuides, Mailer,
    Skill, DiscountSystem, DepositGateway, HiringFee, 
    Currency, Payday, StorageBuckets, TestEmail, 
    AutoLogoutSystem, ExachangeRateAPI
)
from django.conf import settings
from payments.models import PaymentGateway
from teams.models import Team, TeamMember, Invitation
from teams.models import Package as TeamPackage
from proposals . models import Proposal
from projects.models import Project
from analytics.models import NewStats
from marketing.models import AutoTyPist
from pages.models import TermsAndConditions, Hiring, Freelancing, AboutUsPage
from freelancer.models import Freelancer
from client.models import Client
from account.models import Package, Customer, Merchant
from django.contrib.sites.models import Site
# New scripts
from transactions.models import (
    Purchase, ApplicationSale, ProposalSale, 
    ContractSale,ExtContract, SubscriptionItem
)
from location import default_country_state_city


class Command(BaseCommand):
    help = "this creates fixures for the entire system"

    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        
        # COUNTRY, STATE, CITY MODEL
        default_country_state_city()

        # UPDATE SITE MODEL CREATED BY MIGRATION
        site = Site.objects.first()
        site.name='Trosgate Market'
        site.domain = 'localhost'
        site.save()

        # # # ACCOUNT MODEL
        call_command("loaddata", "fixures/db_admin_auth.json")
        call_command("loaddata", "fixures/db_admin_package.json")
        call_command("loaddata", "fixures/global_settings_app.json")

          
        # # MERCHANT AND PAYMENT MODEL
        call_command("loaddata", "fixures/db_payment_gateways.json")
        # # call_command("loaddata", "fixures/db_merchant.json")
        call_command("loaddata", "fixures/db_merchant_api.json")

       # #PLUGINS MODEL
        # call_command("loaddata", "fixures/plugins_app.json")

        # # TEAM MODEL
        # call_command("loaddata", "fixures/db_team_packages.json")

        # #FREELANCER/CLIENT MODEL
        # call_command("loaddata", "fixures/freelancer_app.json")
        # call_command("loaddata", "fixures/db_client.json")
        # call_command("loaddata", "fixures/db_client_account.json")
        # call_command("loaddata", "fixures/db_client_action.json")
        
        # # #TEAM MODEL
        # call_command("loaddata", "fixures/team_app.json")

        # #PROPOSAL MODEL
        # call_command("loaddata", "fixures/proposals_app.json")

        # #PROJECT MODEL
        # call_command("loaddata", "fixures/projects_app.json")


        # # #TRANSACTION MODEL
        # call_command("loaddata", "fixures/transactions_app.json")

        # if not NewStats.objects.count():
        #     call_command("loaddata", "fixures/db_statistics.json")

        
        # if not Hiring.objects.count():
        #     call_command("loaddata", "fixures/db_howitworkhiring.json")
        
        # if not Freelancing.objects.count():
        #     call_command("loaddata", "fixures/db_howitworkfreelancing.json")

        # if not AboutUsPage.objects.count():
        #     call_command("loaddata", "fixures/db_aboutus.json")

        # if not TermsAndConditions.objects.count():
        #     call_command("loaddata", "fixures/db_termsandcond.json")
        
        print('All done')