from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
import resolution
from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale, SalesReporting
from contract.models import InternalContract
from projects.models import Project
from applications.models import Application
from proposals.models import Proposal
from account.models import Customer
from django.http import JsonResponse
from . models import ProjectResolution
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from account.permission import user_is_freelancer, user_is_client




@login_required
def application_resolution(request, application_id, project_slug):
    resolution = ''
    duration_end_time = ''
    application = get_object_or_404(ApplicationSale, pk=application_id, project__slug=project_slug)

    try:
        resolution = ProjectResolution.objects.get(application__pk=application.id, application__team__pk=request.user.freelancer.active_team_id)
        duration_end_time = resolution.end_time

    except:
        print('no such reolution transaction')
    

    context = {
        "application": application,
        "duration_end_time": duration_end_time,
        "resolution": resolution,
        "currency": get_base_currency_code,

    }
    return render(request, "resolution/application_resolution.html", context)


@login_required
@user_is_freelancer
def applicant_start_work(request):
    if request.POST.get('action') == 'start-work':
        applicationsale_id = int(request.POST.get('applicationid'))
        # if request.user.freelancer:
        # if request.user.clients
        application = get_object_or_404(ApplicationSale, pk=applicationsale_id, team__created_by=request.user, purchase__status = Purchase.SUCCESS)
        project = get_object_or_404(Project, pk=application.project.id)
        if ProjectResolution.objects.filter(application=application, project=project, team=application.team).exists():
            print('already started')
            pass
        else:
            ProjectResolution.objects.create(application=application, project=project, team=application.team, start_time=datetime.now())
            print('work started')
        response = JsonResponse({'message': 'It happened'})
        return response







    # days = ''
    # hours = ''
    # minutes = ''
    # seconds = ''
    # duration = ''