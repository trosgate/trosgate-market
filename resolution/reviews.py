from . models import (OneClickReview, ApplicationReview, ProposalReview, ContractReview)
from django.db.models import Avg, F, Count
from proposals.models import Proposal

# REVIEW OF PROPOSAL
def proposal_review_average(team, proposal):
    total_review = ProposalReview.objects.filter(
        resolution__proposal_sale__proposal__team=team, 
        resolution__proposal_sale__proposal=proposal,
        status = True
    ).annotate(
        total_rating=(F("rating")),
        rating_value=(F("rating")),
    ).aggregate(
        proposal_average_rating=(Avg("total_rating")),
        proposal_rating_count=(Count(F("rating_value"))),
    )
    return total_review


def contract_review_average(team, proposal):
    total_review = ContractReview.objects.filter(
        resolution__contract_sale__contract__team=team, 
        resolution__contract_sale__contract__proposal=proposal,
        status = True
    ).annotate(
        total_rating=(F("rating")),
        rating_value=(F("rating")),
    ).aggregate(
        contract_average_rating=(Avg("total_rating")),
        contract_rating_count=(Count(F("rating_value"))),
    )
    return total_review


def oneclick_proposal_review_average(team, proposal):
    total_review = OneClickReview.objects.filter(
        resolution__oneclick_sale__team=team, 
        resolution__oneclick_sale__proposal=proposal,
        status = True
    ).annotate(
        total_rating=(F("rating")),
        rating_value=(F("rating")),
    ).aggregate(
        proposal_average_rating=(Avg("total_rating")),
        proposal_rating_count=(Count(F("rating_value"))),
    )
    return total_review


def oneclick_contract_review_average(team, proposal):
    total_review = OneClickReview.objects.filter(
        resolution__oneclick_sale__team=team, 
        resolution__oneclick_sale__contract__proposal=proposal,
        status = True
    ).annotate(
        total_rating=(F("rating")),
        rating_value=(F("rating")),
    ).aggregate(
        contract_average_rating=(Avg("total_rating")),
        contract_rating_count=(Count(F("rating_value"))),
    )
    return total_review
