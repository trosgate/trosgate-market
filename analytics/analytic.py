from transactions.models import OneClickPurchase, ApplicationSale, Purchase, ProposalSale, ContractSale, SubscriptionItem

from django.db.models import Avg, F, Count, Sum, Aggregate
from proposals.models import Proposal


# SALES RECORD FOR PROPOSAL
def proposal_sales_count_by_proposal(team, proposal):
    total_sales = ProposalSale.objects.filter(
        team=team,
        proposal=proposal,
        purchase__status=Purchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales

def proposal_sales_count_by_contract(team, proposal):
    total_sales = ContractSale.objects.filter(
        team=team,
        contract__proposal=proposal,
        purchase__status=Purchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales

def proposal_oneclick_count_by_proposal(team, proposal):
    total_sales = OneClickPurchase.objects.filter(
        team=team,
        proposal=proposal,
        status=OneClickPurchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales

def proposal_oneclick_count_by_contract(team, proposal):
    total_sales = OneClickPurchase.objects.filter(
        team=team,
        contract__proposal=proposal,
        status=OneClickPurchase.SUCCESS 
    ).aggregate(sales_count=(Count("id")))
    return total_sales


# def contract_review_average(team, proposal):
#     total_review = ContractReview.objects.filter(
#         resolution__contract_sale__contract__team=team, 
#         resolution__contract_sale__contract__proposal=proposal,
#         status = True
#     ).annotate(
#         total_rating=(F("rating")),
#         rating_value=(F("rating")),
#     ).aggregate(
#         contract_average_rating=(Avg("total_rating")),
#         contract_rating_count=(Count(F("rating_value"))),
#     )
#     return total_review