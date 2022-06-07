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
from . models import ProjectResolution, ProjectCompletionFiles, ProjectResolutionReview
from . forms import ProjectCompletionForm
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from account.permission import user_is_freelancer, user_is_client
import mimetypes


@login_required
def application_resolution(request, application_id, project_slug):
    resolution = ''
    duration_end_time = ''
    application = get_object_or_404(ApplicationSale, pk=application_id, project__slug=project_slug)

    completion_form = ProjectCompletionForm(request.POST, request.FILES)
    if request.user.user_type == Customer.FREELANCER:
        if request.user != application.team.created_by:
            return redirect('transactions:application_transaction')

        project_resolution = ProjectResolution.objects.filter(application__pk=application.id, application__team__created_by = request.user, application__team__pk=request.user.freelancer.active_team_id)
        if project_resolution.count() > 0:
            resolution = project_resolution.first()
            duration_end_time = resolution.end_time

        if completion_form.is_valid():
            completed_file = completion_form.save(commit=False)
            completed_file.application = resolution
            completed_file.save()


    elif request.user.user_type == Customer.CLIENT:
        if request.user != application.purchase.client:
            return redirect('transactions:application_transaction')        
        
        project_resolution = ProjectResolution.objects.filter(application__pk=application.id, application__purchase__client = request.user)
        if project_resolution.count() > 0:
            resolution = project_resolution.first()
            duration_end_time = resolution.end_time            


    # for files in ProjectCompletionFiles.objects.filter(team=resolution.team):
    #     attached_files = files.attachment.url


    # fill these variables with real values
    # fl_path = '/media/application/Gladiators/test_file.pdf'

    # filename = ‘downloaded_file_name.extension’

    # fl = open(fl_path, 'r’)
    # mime_type, _ = mimetypes.guess_type(fl_path)
    # response = HttpResponse(fl, content_type=mime_type)
    # response['Content-Disposition'] = "attachment; filename=%s" % filename
    #     return response
    context = {
        "application": application,
        # "attached_files": attached_files,
        "completion_form": completion_form,
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


login_required
@user_is_client
def applicant_review(request):
    if request.POST.get('action') == 'project-review':
        application = int(request.POST.get('application'))
        rating = int(request.POST.get('rating'))
        message = str(request.POST.get('message'))
        print(message)
        print(message, rating)
        print(message, application)

        # res_application = get_object_or_404(ProjectResolution, pk=application)
        # # ProjectResolutionReview
        # print(res_application)

        response = JsonResponse({'message': 'It happened'})
        return response




    # days = ''
    # hours = ''
    # minutes = ''
    # seconds = ''
    # duration = ''