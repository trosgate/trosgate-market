# from teams.models import Team, Package
# from projects.models import Project
# from dateutil.relativedelta import relativedelta
# from proposals.models import Proposal
# from account.models import Customer
# from datetime import timedelta
# from django.utils import timezone
# from applications.models import Application
# from contract.models import InternalContract



# def one_month():
#     return (timezone.now() + relativedelta(months = 1))


# class PackageController():
#     """
#     This is the base class for controlling teams and their packages
#     """
#     def __init__(self, team):
#         self.team = team



#     def monthly_projects_applicable_per_team(self):
#         team_project_limit = self.team.package.monthly_projects_applicable_per_team
#         monthly_applications_count = Application.objects.filter(
#             team=self.team, 
#             created_at__gt=timezone.now() - relativedelta(months=1)
#         ).count()          

#         return team_project_limit > monthly_applications_count


#     def monthly_offer_contracts(self):
#         team_contracts_limit = self.team.package.monthly_offer_contracts_per_team
#         monthly_team_contracts_count = InternalContract.objects.filter(
#             team=self.team,
#             date_created__gt=timezone.now() - relativedelta(months=1)
#         ).count()          

#         return team_contracts_limit > monthly_team_contracts_count




















