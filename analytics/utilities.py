
from datetime import datetime
from teams.models import Tracking


def get_user_team_and_date_tracking(team, user, date):
    trakings = Tracking.objects.filter(team=team, created_by=user, created_at__date=date, is_tracked=True)
    return sum(tracker.minutes for tracker in trakings)

def get_team_and_month_tracking(team, month):
    trakings = Tracking.objects.filter(team=team, created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(tracker.minutes for tracker in trakings)

def get_user_team_and_proposal_and_month_tracking(team, proposal, user, month):
    trakings = Tracking.objects.filter(team=team, proposal=proposal, created_by=user, created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(tracker.minutes for tracker in trakings)

def get_user_team_and_month_tracking(team, user, month):
    trakings = Tracking.objects.filter(team=team, created_by=user, created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(tracker.minutes for tracker in trakings)

def get_time_for_user_team_and_month_tracking(team, user, month):
    trakings = Tracking.objects.filter(team=team, created_by=user, created_at__year=month.year, created_at__month=month.month, is_tracked=True)
    return sum(tracker.minutes for tracker in trakings)






















































































