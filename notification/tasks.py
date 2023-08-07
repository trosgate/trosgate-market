from account.models import Customer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from general_settings.backends import get_website_email
from celery import shared_task
from trosgate.celery import app
from django.utils import timezone
from datetime import timedelta
from django.apps import apps
from celery.schedules import crontab
from .mailer import credit_pending_balance_email


@shared_task
def send_pending_balance_email(account_id, paid_amount, purchase_model, purchase_id):
    from proposals.models import Proposal
    from projects.models import Project
    from freelancer.models import FreelancerAccount
    from contract.models import InternalContract, Contract
    

    account = FreelancerAccount.objects.get(pk=account_id)
    if purchase_model == 'proposal':
        purchase = Proposal.objects.get(pk=purchase_id)
    elif purchase_model == 'project':
        purchase = Project.objects.get(pk=purchase_id)
    elif purchase_model == 'contract':
        purchase = InternalContract.objects.get(pk=purchase_id)
    elif purchase_model == 'excontract':
        purchase = Contract.objects.get(pk=purchase_id)
    else:
        raise ValueError("Invalid purchase_model provided.")
    
    credit_pending_balance_email(account, paid_amount, purchase_model, purchase)



# @app.task #for periodic tasks
# def send_periodic_emailxxxx(account_id, pending_balance, purchase_id, subject):

#     pass






















































































