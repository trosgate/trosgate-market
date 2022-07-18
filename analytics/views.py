import random
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import F, Q
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.http import JsonResponse
from account.permission import user_is_freelancer
from proposals.models import Proposal
from account.models import Customer
from teams.models import Team, AssignMember, Tracking
from .utilities import (
    get_user_team_and_date_tracking, 
    get_team_and_month_tracking, 
    get_user_team_and_proposal_and_month_tracking, 
    get_user_team_and_month_tracking, 
    get_time_for_user_team_and_month_tracking,
    )

@login_required
@user_is_freelancer
def time_tracker(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    proposals = team.proposalteam.all()
    members = team.members.all()

    #team member date
    num_of_days = int(request.GET.get('num_of_days', 0))
    date_of_user = timezone.now() - timedelta(days = num_of_days)
    date_tracking = Tracking.objects.filter(team=team, created_by=request.user, created_at__date=date_of_user, is_tracked=True)

    week_span = int(request.GET.get(7, 7))
    week_ago = timezone.now() - timedelta(days=week_span)
    week_tracking = Tracking.objects.filter(team=team, created_by=request.user, created_at__date__gte=week_ago, is_tracked=True)

    #user date, proposal and month
    num_of_month = int(request.GET.get('num_of_month', 0))
    month_of_user = timezone.now() - relativedelta(month = num_of_month)

    for proposal in proposals:
        proposal.user_team_and_proposal_and_month_tracking = get_user_team_and_proposal_and_month_tracking(team, proposal, request.user, month_of_user)

    #team member date and month
    team_month = int(request.GET.get('team_month', 0))
    month_of_team_members = timezone.now() - relativedelta(month = team_month)

    for member in members:
        member.time_for_user_team_and_month_tracking = get_time_for_user_team_and_month_tracking(team, member, month_of_team_members)

    context={
        'team':team,
        'proposals':proposals,
        'members':members,
        'num_of_days':num_of_days,
        'date_of_user':date_of_user,
        'date_tracking':date_tracking,
        'num_of_month':num_of_month,
        'month_of_user':month_of_user,
        'team_month':team_month,
        'month_of_team_members':month_of_team_members,
        'team_and_month_tracking':get_team_and_month_tracking(team, month_of_team_members),
        'user_team_and_month_tracking':get_user_team_and_month_tracking(team, request.user, month_of_user),
        'user_team_and_date_tracking':get_user_team_and_date_tracking(team, request.user, date_of_user),
    }
    return render(request, 'analytics/tracker_board.html', context)