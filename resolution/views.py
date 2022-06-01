from django.shortcuts import render
from datetime import datetime, timezone, timedelta

# Create your views here.

def time_duration(request):
    # go live date = 2022/08/15
    duration = datetime(2022, 08, 15, tzinfo=timezone.utc) - timezone.now()
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds // 60) % 60
    seconds = duration.seconds % 60

    context = {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
    }
    return render(request, "transactions/application_sales.html", context)

# @login_required
# @user_is_freelancer
# def application_sales(request, project_slug):
#     team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
#     project = get_object_or_404(Project, slug=project_slug, status=Project.ACTIVE)
#     application_sales = project.applicantprojectapplied.filter(team=team, purchase__status=Purchase.SUCCESS)

#     context = {
#         "application_sales": application_sales,
#     }
#     return render(request, "transactions/application_sales.html", context)

