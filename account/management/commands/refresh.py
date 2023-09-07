from django.core.management.base import BaseCommand
from django.core.management import call_command
from account.models import Country, Package, Customer
from transactions.models import Purchase, ProposalSale


class Command(BaseCommand):
    help = "this refreshes the system"

    def handle(self, *args, **kwargs):
        # call_command("makemigrations")
        # call_command("migrate")

        # call_command("loaddata", "fixures/transactions_app.json")
        Purchase.objects.all().delete()
        # for proposal in ProposalSale.objects.all():
        #     proposal.save()
        print('This command is done')