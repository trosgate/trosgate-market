from transactions.models import OneClickPurchase, ApplicationSale, Purchase, ProposalSale, ContractSale, SubscriptionItem
from django.db.models import Avg, F, Count, Sum, Aggregate
from resolution.models import (
    OneClickReview, 
    ApplicationReview, 
    ProposalReview, 
    ContractReview,
    OneClickResolution,
    ProjectResolution,
    ProposalResolution,
    ContractResolution,
    ExtContractResolution
)
from proposals.models import Proposal
from freelancer.models import Freelancer
from client.models import Client
from teams.models import Team
from projects.models import Project
from applications.models import Application
from transactions.models import OneClickPurchase, Purchase
from contract.models import InternalContract, Contract
from django.utils import timezone

def ongoing_founder_projects(team):
    one_click_tasks = OneClickResolution.objects.filter(team=team, status='ongoing').count()
    roposal_tasks = ProposalResolution.objects.filter(team=team, status='ongoing').count()
    applied_tasks = ProjectResolution.objects.filter(team=team, status='ongoing').count()
    int_contract_tasks = ContractResolution.objects.filter(team=team, status='ongoing').count()
    ext_contract_tasks = ExtContractResolution.objects.filter(team=team, status='ongoing').count()
 
    return one_click_tasks + roposal_tasks + applied_tasks + int_contract_tasks + ext_contract_tasks

def cancelled_founder_projects(team):
    one_click_tasks = OneClickResolution.objects.filter(team=team, status='cancelled').count()
    proposal_tasks = ProposalResolution.objects.filter(team=team, status='cancelled').count()
    applied_tasks = ProjectResolution.objects.filter(team=team, status='cancelled').count()
    int_contract_tasks = ContractResolution.objects.filter(team=team, status='cancelled').count()
    ext_contract_tasks = ExtContractResolution.objects.filter(team=team, status='cancelled').count()
  
    return one_click_tasks + proposal_tasks + applied_tasks + int_contract_tasks + ext_contract_tasks

def completed_founder_projects(team):
    one_click_tasks = OneClickResolution.objects.filter(team=team, status='completed').count()
    proposal_tasks = ProposalResolution.objects.filter(team=team, status='completed').count()
    applied_tasks = ProjectResolution.objects.filter(team=team, status='completed').count()
    int_contract_tasks = ContractResolution.objects.filter(team=team, status='completed').count()
    ext_contract_tasks = ExtContractResolution.objects.filter(team=team, status='completed').count()

    return one_click_tasks + proposal_tasks + applied_tasks + int_contract_tasks + ext_contract_tasks

def total_verified_sale(team):
    proposal_total_sales = ProposalSale.objects.filter(team=team, purchase__status='success').count() 
    contract_total_sales = ContractSale.objects.filter(team=team, purchase__status='success').count() 
    application_total_sales = ApplicationSale.objects.filter(team=team, purchase__status='success').count() 
    oneclick_total_sales = OneClickPurchase.objects.filter(team=team, status='success').count() 
    
    return proposal_total_sales + contract_total_sales + application_total_sales +oneclick_total_sales


def total_projects_in_queue(team):
    started = ongoing_founder_projects(team) + completed_founder_projects(team) + cancelled_founder_projects(team)
    all_tasks = total_verified_sale(team)
    return int(all_tasks - started)

def user_review_rate(team):
    proposal_reviews = ProposalReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()
    contract_reviews = ContractReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()
    oneclick_review = OneClickReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()
    application_review = ApplicationReview.objects.filter(resolution__team=team, status=True, rating__gte=3).count()

    totals = proposal_reviews + contract_reviews + contract_reviews + oneclick_review + application_review
    return totals

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

# ONECLICK-PROPOSAL SALES RECORD FOR PROPOSAL
def proposal_oneclick_count_by_proposal(team, proposal):
    total_sales = OneClickPurchase.objects.filter(
        team=team,
        proposal=proposal,
        status=OneClickPurchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales

# ONECLICK-CONTRACT SALES RECORD FOR PROPOSAL
def proposal_oneclick_count_by_contract(team, proposal):
    total_sales = OneClickPurchase.objects.filter(
        team=team,
        contract__proposal=proposal,
        status=OneClickPurchase.SUCCESS 
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
    oneclick_hire = OneClickPurchase.objects.filter(status='success').exclude(category='externalcontract').count()
    return direct_proposal + intern_contract + oneclick_hire

def total_proposal_review_rate():
    proposal_reviews = ProposalReview.objects.filter(status=True).count()
    contract_reviews = ContractReview.objects.filter(status=True).count()
    oneclick_proposal_rev = OneClickReview.objects.filter(
        status=True,
        resolution__oneclick_sale__category='proposal'
    ).count()
    oneclick_contract_rev = OneClickReview.objects.filter(
        status=True,
        resolution__oneclick_sale__category='contract'
    ).count()
    return proposal_reviews + contract_reviews + oneclick_proposal_rev + oneclick_contract_rev

def total_internal_contracts():
    return InternalContract.objects.all().count()

def total_external_contracts():
    return Contract.objects.all().count()

def total_contracts_hired():
    int_contracts = InternalContract.objects.filter(reaction='paid').count()
    ext_contracts = Contract.objects.filter(reaction='paid').count()
    return int_contracts + ext_contracts



































