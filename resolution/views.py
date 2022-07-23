from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
from contract.models import InternalContract
from projects.models import Project
from applications.models import Application
from proposals.models import Proposal
from account.models import Customer
from django.http import JsonResponse
from . forms import ProjectCompletionForm, ProposalCompletionForm
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from account.permission import user_is_freelancer, user_is_client
import mimetypes
from django.utils import timezone
from account.fund_exception import ReviewException
from transactions.models import (
    ApplicationSale, 
    Purchase, 
    ProposalSale, 
    ContractSale
)
from . models import (
    ProjectResolution,
    ProposalResolution, 
    ProjectCompletionFiles, 
    ProposalCompletionFiles, 
    ApplicationReview,
    ProposalReview
)



@login_required
def application_resolution(request, application_id, project_slug):
    resolution = ''
    duration_end_time = ''
    application = get_object_or_404(ApplicationSale, pk=application_id, project__slug=project_slug)
    client_review = ApplicationReview.objects.all()

    completion_form = ProjectCompletionForm(request.POST, request.FILES)
    if request.user.user_type == Customer.FREELANCER:
        if request.user != application.team.created_by:
            return redirect('transactions:application_transaction')

        project_resolution = ProjectResolution.objects.filter(application=application, application__team__created_by = request.user, application__team__pk=request.user.freelancer.active_team_id)
        if project_resolution.count() > 0:
            resolution = project_resolution.first()
            duration_end_time = resolution.end_time

        if resolution and completion_form.is_valid():
            completed_file = completion_form.save(commit=False)
            completed_file.application = resolution
            completed_file.save()


    elif request.user.user_type == Customer.CLIENT:
        if request.user != application.purchase.client:
            return redirect('transactions:application_transaction')        
        
        project_resolution = ProjectResolution.objects.filter(application=application, application__purchase__client = request.user)
        if project_resolution.count() > 0:
            resolution = project_resolution.first()
            duration_end_time = resolution.end_time            

    context = {
        "application": application,
        "client_review": client_review,
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
        response = JsonResponse({'message': 'work started'})
        return response


login_required
@user_is_client
def applicant_review(request):
    success_or_error_message = ''
    error_messages = ''
    if request.POST.get('action') == 'project-review':
        application_id = int(request.POST.get('applicationid'))
        rating = int(request.POST.get('rating'))
        title = str(request.POST.get('title'))
        message = str(request.POST.get('message'))

        application = get_object_or_404(ApplicationSale, pk=application_id, purchase__client = request.user, purchase__status = Purchase.SUCCESS)
        project = get_object_or_404(Project, pk=application.project.id)
        resolution = get_object_or_404(ProjectResolution, application=application, project=project, team=application.team)

        reviews = ApplicationReview.objects.filter(resolution=resolution, status=True)
        if reviews.count() > 0:
            review = reviews.first()
            review.application = resolution
            review.title = title
            review.message = message
            review.rating = rating
            review.status = True
            review.save()
            success_or_error_message = 'Your review updated successfully'
        else:
            try:
                ApplicationReview.objects.create(resolution=resolution, title=title, message=message, rating=rating, status=True)
                success_or_error_message = 'Review received Successfully'
            except Exception as e:
                error_messages = str(e)
                success_or_error_message = f'Ooops! {error_messages}'

        response = JsonResponse({'success_or_error_message': success_or_error_message})
        return response


@login_required
def proposal_resolution(request, proposal_id, proposal_slug):
    resolution = ''
    duration_end_time = ''
    proposal_sold = get_object_or_404(ProposalSale, pk=proposal_id, proposal__slug=proposal_slug)
    client_review = ProposalReview.objects.filter(resolution__proposal_sale=proposal_sold)

    completion_form = ProposalCompletionForm(request.POST, request.FILES)
    if request.user.user_type == Customer.FREELANCER:
        if request.user != proposal_sold.team.created_by:
            return redirect('transactions:application_transaction')

        proposal_resolution = ProposalResolution.objects.filter(proposal_sale__pk=proposal_sold.id, proposal_sale__team__created_by = request.user, proposal_sale__team__pk=request.user.freelancer.active_team_id)
        if proposal_resolution.count() > 0:
            resolution = proposal_resolution.first()
            duration_end_time = resolution.end_time

        # if resolution and completion_form.is_valid():
        #     completed_file = completion_form.save(commit=False)
        #     completed_file.proposal_sale = resolution
        #     completed_file.save()


    elif request.user.user_type == Customer.CLIENT:
        if request.user != proposal_sold.purchase.client:
            return redirect('transactions:proposal_transaction')        
        
        proposal_resolution = ProposalResolution.objects.filter(proposal_sale=proposal_sold, proposal_sale__purchase__client = request.user)
        if proposal_resolution.count() > 0:
            resolution = proposal_resolution.first()
            duration_end_time = resolution.end_time            

    context = {
        "proposal_sold": proposal_sold,
        "client_review": client_review,
        "completion_form": completion_form,
        "duration_end_time": duration_end_time,
        "resolution": resolution,
        "currency": get_base_currency_code,

    }
    return render(request, "resolution/proposal_resolution.html", context)


@login_required
@user_is_freelancer
def proposal_start_work(request):
    if request.POST.get('action') == 'start-work':
        proposalsale_id = int(request.POST.get('proposalSoldId'))

        proposal_sold = get_object_or_404(ProposalSale, pk=proposalsale_id, team__created_by=request.user, purchase__status = Purchase.SUCCESS)
        if ProposalResolution.objects.filter(proposal_sale=proposal_sold, team=proposal_sold.team).exists():
            print('already started')
            pass
        else:
            ProposalResolution.objects.create(proposal_sale=proposal_sold, team=proposal_sold.team, start_time=timezone.now())
            print('work started')
        response = JsonResponse({'message': 'work started'})
        return response


login_required
@user_is_client
def proposal_review(request):
    success_or_error_message = ''
    error_messages = ''
    if request.POST.get('action') == 'proposal-review':
        proposal_sold_id = int(request.POST.get('proposalSoldId'))
        rating = int(request.POST.get('rating'))
        title = str(request.POST.get('title'))
        message = str(request.POST.get('message'))

        proposal_sale = get_object_or_404(ProposalSale, pk=proposal_sold_id, purchase__client = request.user, purchase__status = Purchase.SUCCESS)
        resolution = get_object_or_404(ProposalResolution, proposal_sale=proposal_sale, team=proposal_sale.team)

        reviews = ProposalReview.objects.filter(resolution=resolution, status=True)
        if reviews.count() > 0:
            review = reviews.first()
            review.resolution = resolution
            review.title = title
            review.message = message
            review.rating = rating
            review.status = True
            review.save()
            success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review modified Successfully</span>'
        else:
            try:
                ProposalReview.objects.create(resolution=resolution, title=title, message=message, rating=rating, status = True)
                success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
            except Exception as e:
                error_messages = str(e)
                success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

        response = JsonResponse({'success_or_error_message': success_or_error_message})
        return response


# login_required
# @user_is_client
# def applicant_review(request):
#     success_or_error_message = ''
#     error_messages = ''
#     if request.POST.get('action') == 'project-review':
#         application_id = int(request.POST.get('applicationid'))
#         rating = int(request.POST.get('rating'))
#         title = str(request.POST.get('title'))
#         message = str(request.POST.get('message'))

#         application = get_object_or_404(ApplicationSale, pk=application_id, purchase__client = request.user, purchase__status = Purchase.SUCCESS)
#         project = get_object_or_404(Project, pk=application.project.id)
#         resolution = get_object_or_404(ProjectResolution, application=application, project=project, team=application.team)

#         reviews = ApplicationReview.objects.filter(resolution=resolution, status=True)
#         if reviews.count() > 0:
#             review = reviews.first()
#             review.application = resolution
#             review.title = title
#             review.message = message
#             review.rating = rating
#             review.status = True
#             review.save()
#             success_or_error_message = 'Your review updated successfully'
#         else:
#             try:
#                 ApplicationReview.create(resolution=resolution, title=title, message=message, rating=rating, status=True)
#                 success_or_error_message = 'Review received Successfully'
#             except ReviewException as e:
#                 error_messages = str(e)
#                 success_or_error_message = f'Ooops! {error_messages}'

#         response = JsonResponse({'success_or_error_message': success_or_error_message})
#         return response