from django.core.management import call_command
from django.core.management.base import BaseCommand
from account.models import Country, Customer
from general_settings . models import (
    WebsiteSetting, Category, Department, Size, PaymentsControl,
    Skill, DiscountSystem, PaymentGateway, HiringFee, Currency, Payday
)
from teams . models import Package, Team
from proposals . models import Proposal
from projects.models import Project


class Command(BaseCommand):
    help = "this creates default values via commands for the entire system"

    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")

        if not Country.objects.count():
            call_command("loaddata", "db_countries.json")

        if not Customer.objects.count():
            call_command("loaddata", "db_admin_auth.json")
            call_command("loaddata", "db_client_auth.json")
            # call_command("loaddata", "db_freelancer_auth.json")

        if not WebsiteSetting.objects.count():
            call_command("loaddata", "db_admin_settings.json")

        if not DiscountSystem.objects.count():
            call_command("loaddata", "db_discount_system.json")

        if not HiringFee.objects.count():
            call_command("loaddata", "db_freelancer_fee.json")

        if not Package.objects.count():
            call_command("loaddata", "db_packages.json")

        if not Category.objects.count():
            call_command("loaddata", "db_categories.json")

        if not Skill.objects.count():
            call_command("loaddata", "db_skills.json")

        if not Size.objects.count():
            call_command("loaddata", "db_business_size.json")

        if not Department.objects.count():
            call_command("loaddata", "db_department.json")

        if not PaymentGateway.objects.count():
            call_command("loaddata", "db_payment_gateways.json")

        if not Payday.objects.count():
            call_command("loaddata", "db_payday.json")

        if not Currency.objects.count():
            call_command("loaddata", "db_currencies.json")

        if not PaymentsControl.objects.count():
            call_command("loaddata", "db_fund_control.json")

        if not Project.objects.count():
          call_command("loaddata", "db_projects.json")

        # if not Proposals.objects.count():
            # call_command("loaddata", "db_proposals.json")
        