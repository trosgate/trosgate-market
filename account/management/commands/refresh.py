from django.core.management.base import BaseCommand
from django.core.management import call_command
from proposals.models import Proposal
from projects.models import Project
from transactions.models import Purchase, ProposalSale
from contract.models import Contract
import copy
import uuid
from contract.models import Contractor


class Command(BaseCommand):
    help = "this refreshes the system"

    def handle(self, *args, **kwargs):
        # call_command("makemigrations")
        # call_command("migrate")
        
        # proposal = Proposal.objects.get(pk=1)

        # new_proposal = Proposal()

        # # Clone the attributes from the existing object
        # new_proposal.__dict__.update(proposal.__dict__)

        # # Modify the attributes you want to change
        # new_proposal.title = 'I am expert in content writing and publishing on Facebook'
        # new_proposal.pk = 8
        # new_proposal.merchant_id = 2
        # new_proposal.created_by_id = 18
        # new_proposal.identifier = ''
        # new_proposal.reference = ''
        # new_proposal.save()

        ## assign to different user
        print('This command is done')