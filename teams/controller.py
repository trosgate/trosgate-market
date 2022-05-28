import requests
from django.shortcuts import redirect, get_object_or_404
from teams.models import Team
from projects.models import Project
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from proposals.models import Proposal
from account.models import Customer

# this function is complete now
def max_member_per_team(team):
    invites_per_team = team.package.max_member_per_team > team.members.count()
    return invites_per_team

# this function is complete now but yet to add template limit
def max_proposals_allowable_per_team(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    team_proposal_limit = team.package.max_proposals_allowable_per_team  
    team_proposals_count = team.proposalteam.count()
    max_proposal_per_team = team_proposal_limit > team_proposals_count
    return max_proposal_per_team

# this function is ongoing ............ 
def monthly_offer_contracts(team):
    team_contracts_limit = team.package.monthly_offer_contracts_per_team
    monthly_team_contracts_count = team.internalcontractteam.filter(
        date_created__gt=datetime.now() - relativedelta(month=1)
        ).count()

    offer_contracts_per_team = team_contracts_limit > monthly_team_contracts_count
    return offer_contracts_per_team

def monthly_projects_applicable_per_team(request):
    if request.user.is_authenticated and request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
        team_application_limit = team.package.monthly_projects_applicable_per_team  
        monthly_applications_count = team.applications.filter(
            project__status = Project.ACTIVE, 
            created_at__gt=datetime.now() - relativedelta(month=1)
            ).count()
        print(team_application_limit)
        print(monthly_applications_count)
        monthly_project_application = team_application_limit > monthly_applications_count

        return monthly_project_application
    return None


# def daily_Handshake_mails_to_clients(request):
#     team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
#     team_proposal_limit = team.package.max_proposals_allowable_per_team  
#     team_proposals_count = team.proposal.count()

#     print(team_proposal_limit)
#     print(team_proposals_count)

#     proposal_per_team = team_proposal_limit > team_proposals_count
#     print(proposal_per_team)
#     return proposal_per_team
