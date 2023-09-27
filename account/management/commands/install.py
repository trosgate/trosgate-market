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
from contract.models import Contract

class Command(BaseCommand):
    help = "this creates fixures for the entire system"

    def handle(self, *args, **kwargs):
        # call_command("makemigrations")
        # call_command("migrate")
        
        # COUNTRY, STATE, CITY MODEL
        # default_country_state_city()

        # UPDATE SITE MODEL CREATED BY MIGRATION
        # site = Site.objects.get(pk=1)
        # site.name='Trosgate Market'
        # site.domain = 'localhost'
        # site.save()
        # Customer.objects.filter(user_type='merchant').delete()
        # domain = ['gladiators.localhost', 'legend.localhost', 'youtubers.localhost', 'facebookr.localhost']
        # name = ['Gladiators', 'Legend', 'Youtubers', 'Facebookr']

        # for dom, nam in zip(domain, name):
        #     Site.objects.create(domain=dom, name=nam)

        # # # ACCOUNT MODEL
        call_command("loaddata", "fixures/db_admin_auth.json")
        call_command("loaddata", "fixures/db_admin_package.json")
        call_command("loaddata", "fixures/db_global_settings.json")
        # call_command("loaddata", "fixures/db_plugins.json")
        call_command("loaddata", "fixures/db_merchant.json")
        call_command("loaddata", "fixures/db_payments.json")
        call_command("loaddata", "fixures/db_freelancer.json")
        call_command("loaddata", "fixures/db_client.json")
        call_command("loaddata", "fixures/db_teams.json")
        call_command("loaddata", "fixures/db_proposals.json")
        call_command("loaddata", "fixures/db_projects.json")

        print('All done')