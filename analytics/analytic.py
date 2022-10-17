from transactions.models import OneClickPurchase, ApplicationSale, Purchase, ProposalSale, ContractSale, SubscriptionItem
from django.db.models import Avg, F, Count, Sum, Aggregate
from resolution.models import OneClickReview, ApplicationReview, ProposalReview, ContractReview
from proposals.models import Proposal
from freelancer.models import Freelancer
from client.models import Client
from teams.models import Team
from projects.models import Project
from applications.models import Application
from transactions.models import OneClickPurchase, Purchase
from contract.models import InternalContract, Contract


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



































