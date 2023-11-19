from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale
from django.db.models import Avg, F, Count, Sum, Aggregate
from resolution.models import (
    # ApplicationReview, 
    # ProposalReview, 
    # ContractReview,
    # ProjectResolution,
    ProposalJob,
    # ContractResolution,
    # ExtContractResolution
)
from proposals.models import Proposal
from freelancer.models import Freelancer
from client.models import Client
from teams.models import Team
from projects.models import Project
from applications.models import Application
from transactions.models import  Purchase
from contract.models import Contract
from django.utils import timezone

def ongoing_founder_projects(team):
    # roposal_tasks = ProposalJob.objects.filter(team=team, status='ongoing').count()
    # applied_tasks = ProjectResolution.objects.filter(team=team, status='ongoing').count()
    # int_contract_tasks = ContractResolution.objects.filter(team=team, status='ongoing').count()
    # ext_contract_tasks = ExtContractResolution.objects.filter(team=team, status='ongoing').count()
 
    # return roposal_tasks + applied_tasks + int_contract_tasks + ext_contract_tasks
    return 0

def cancelled_founder_projects(team):
    # proposal_tasks = ProposalJob.objects.filter(team=team, status='cancelled').count()
    # applied_tasks = ProjectResolution.objects.filter(team=team, status='cancelled').count()
    # int_contract_tasks = ContractResolution.objects.filter(team=team, status='cancelled').count()
    # ext_contract_tasks = ExtContractResolution.objects.filter(team=team, status='cancelled').count()
  
    # return proposal_tasks + applied_tasks + int_contract_tasks + ext_contract_tasks
    return 0

def completed_founder_projects(team):
    # proposal_tasks = ProposalJob.objects.filter(team=team, status='completed').count()
    # applied_tasks = ProjectResolution.objects.filter(team=team, status='completed').count()
    # int_contract_tasks = ContractResolution.objects.filter(team=team, status='completed').count()
    # ext_contract_tasks = ExtContractResolution.objects.filter(team=team, status='completed').count()

    # return proposal_tasks + applied_tasks + int_contract_tasks + ext_contract_tasks
    return 0


def total_verified_sale(team):
    proposal_total_sales = ProposalSale.objects.filter(team=team, purchase__status='success').count() 
    contract_total_sales = ContractSale.objects.filter(team=team, purchase__status='success').count() 
    application_total_sales = ApplicationSale.objects.filter(team=team, purchase__status='success').count() 

    return proposal_total_sales + contract_total_sales + application_total_sales


def total_projects_in_queue(team):
    started = ongoing_founder_projects(team) + completed_founder_projects(team) + cancelled_founder_projects(team)
    all_tasks = total_verified_sale(team)
    return int(all_tasks - started)

def user_review_rate(team):
    # proposal_reviews = ProposalReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()
    # contract_reviews = ContractReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()
    # application_review = ApplicationReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()

    # totals = proposal_reviews + contract_reviews + contract_reviews + application_review
    # return totals
    return 0

# PROPOSAL SALES RECORD FOR PROPOSAL
def proposal_sales_count_by_proposal(team, proposal):
    total_sales = ProposalSale.objects.filter(
        team=team,
        proposal=proposal,
        purchase__status=Purchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales

# CONTRACT SALES RECORD FOR PROPOSAL
def proposal_sales_count_by_contract(team, proposal):
    total_sales = ContractSale.objects.filter(
        team=team,
        contract__proposal=proposal,
        purchase__status=Purchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales


def total_freelancers():
    return Freelancer.objects.all().count()

def total_clients():
    return Client.objects.all().count()

def total_teams():
    return Team.objects.all().count()

def total_projects():
    return Project.objects.all().count()

def total_projects_reopen():
    return Project.objects.filter(reopen_count=1).count()

def total_projects_reopen():
    return Project.objects.filter(reopen_count=1).count()

def total_project_hired():
    return Purchase.objects.filter(category='project', status='success').count()

def total_proposals():
    return Proposal.objects.all().count()

def total_proposal_hired():
    direct_proposal = Purchase.objects.filter(category='proposal', status='success').count()
    intern_contract = Purchase.objects.filter(category='contract', status='success').count()
    return direct_proposal + intern_contract

def total_proposal_review_rate():
    # proposal_reviews = ProposalReview.objects.filter(status=True).count()
    # contract_reviews = ContractReview.objects.filter(status=True).count()
    # return proposal_reviews + contract_reviews
    return 0

def total_internal_contracts():
    # return InternalContract.objects.all().count()
    return Contract.objects.all().count()

def total_external_contracts():
    return Contract.objects.all().count()

def total_contracts_hired():
    ext_contracts = Contract.objects.filter(reaction='paid').count()
    return ext_contracts



































