from .models import Team
from account.models import Customer


def active_team(request):
    if request.user.is_authenticated and request.user.user_type == Customer.FREELANCER:
        if request.user.freelancer.active_team_id:
            teams = Team.objects.get(pk=request.user.freelancer.active_team_id)
            return {'active_team':teams}

    return {'active_team':None}

