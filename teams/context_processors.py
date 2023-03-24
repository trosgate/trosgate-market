from django.conf import settings
from django.core.cache import cache
from .models import Team
from account.models import Customer


def active_team(request):
    if request.user.is_authenticated and request.user.user_type == Customer.FREELANCER:
        cache_key = f'team_queryset_{request.user.freelancer.active_team_id}'
        teams = cache.get(cache_key)
        if teams:
            return {'active_team':teams}
        
        elif teams is None and request.user.freelancer.active_team_id:
            teams = Team.objects.get(pk=request.user.freelancer.active_team_id)
            cache.set(cache_key, teams, settings.CACHE_TTL)
            return {'active_team':teams}

    return {'active_team':None}

