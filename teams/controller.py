import requests
from django.shortcuts import redirect, get_object_or_404
from teams.models import Team
from projects.models import Project
from dateutil.relativedelta import relativedelta
from proposals.models import Proposal
from account.models import Customer
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from applications.models import Application

# max_proposals_allowable_per_team
# monthly_projects_applicable_per_team
# monthly_offer_contracts_per_team
# daily_Handshake_mails_to_clients
def one_month():
    return (timezone.now() + relativedelta(months = 1))


class PackageController():
    """
    This is the base class for controlling teams and their packages
    """
    def __init__(self, team):
        self.team = team

    def max_member_per_team(self):
        # Must return a Bool:True. If True, the team has chances to invite
        max_member_in_a_team = self.team.package.max_member_per_team > self.team.members.count()
        return max_member_in_a_team

    # this function is complete now but yet to add template limit
    def max_proposals_allowable_per_team(self):
        team_proposal_limit = self.team.package.max_proposals_allowable_per_team  
        team_proposals_count = self.team.proposalteam.count()
        return team_proposal_limit > team_proposals_count

    def monthly_projects_applicable_per_team(self):
        team_project_limit = self.team.package.monthly_projects_applicable_per_team
        monthly_applications_count = Application.objects.filter(
            team=self.team, 
            created_at__gt=timezone.now() - relativedelta(months=1)
        ).count()          

        return team_project_limit > monthly_applications_count

        # print('team_project_limit:', team_project_limit, ':', self.team.title)
        # print('monthly_applications_count:', monthly_applications_count)

def monthly_offer_contracts(team):
    team_contracts_limit = team.package.monthly_offer_contracts_per_team
    monthly_team_contracts_count = team.internalcontractteam.filter(
        date_created__gt=timezone.now() - relativedelta(month=1)
        ).count()

    offer_contracts_per_team = team_contracts_limit > monthly_team_contracts_count
    return offer_contracts_per_team






# def max_member_per_team(team):
#     invites_per_team = team.package.max_member_per_team > team.members.count()
#     return invites_per_team


# def max_proposals_allowable_per_team(request):
#     team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
#     team_proposal_limit = team.package.max_proposals_allowable_per_team  
#     team_proposals_count = team.proposalteam.count()
#     max_proposal_per_team = team_proposal_limit > team_proposals_count
#     return max_proposal_per_team


















