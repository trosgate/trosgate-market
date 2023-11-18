from django.conf import settings
from django.core.cache import cache
from .models import Team
from account.models import Customer
from django.shortcuts import get_object_or_404



def active_team(request):
    active_team = None

    if request.user.is_authenticated and request.user.user_type == Customer.FREELANCER:
        cache_key = f'team_queryset_{request.user.freelancer.active_team_id}'
        active_team = cache.get(cache_key)

        if active_team is None and request.user.freelancer.active_team_id:
            # Use get_object_or_404 for better readability and to handle the case of a non-existing team
            active_team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id)

            # Set the team in the cache with a TTL
            cache.set(cache_key, active_team, settings.CACHE_TTL)

    return {'active_team': active_team}

