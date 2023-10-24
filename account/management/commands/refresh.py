from django.core.management.base import BaseCommand
from django.core.management import call_command
from proposals.models import Proposal
from projects.models import Project
from transactions.models import Purchase, ProposalSale
from contract.models import Contract
import copy
import uuid
from contract.models import Contractor
from threadlocals.threadlocals import get_thread_variable



class Command(BaseCommand):
    help = "this refreshes the system"

    def handle(self, *args, **kwargs):
        # call_command("makemigrations")
        # call_command("migrate")
        
        Purchase.objects.filter(merchant_id=13).delete()

        print('This command is done')