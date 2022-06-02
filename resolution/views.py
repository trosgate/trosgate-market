from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale, SalesReporting
from contract.models import InternalContract
from projects.models import Project
from applications.models import Application
from proposals.models import Proposal
from account.models import Customer
# Create your views here.


@login_required
def application_resolution(request, application_id, project_slug):
    days = ''
    hours = ''
    minutes = ''
    seconds = ''
    duration = ''
    if request.user.user_type == Customer.FREELANCER:    
        applcation = get_object_or_404(ApplicationSale, pk=application_id, project__slug=project_slug)
        duration = datetime('2022, 08, 15', tzinfo=timezone.utc) - timezone.now()
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
    return render(request, "resolution/application_resolution.html", context)


