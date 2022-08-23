from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from contract.models import InternalContract
from projects.models import Project
from applications.models import Application
from proposals.models import Proposal
from account.models import Customer
from django.http import JsonResponse
from . forms import ProjectCompletionForm, ProposalCompletionForm, ContractCompletionForm
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from account.permission import user_is_freelancer, user_is_client
import mimetypes
from django.utils import timezone
from account.fund_exception import ReviewException
from transactions.models import (
    Purchase, 
    ProposalSale, 
    ContractSale,
    ApplicationSale 
)
from . models import (
    ProjectResolution,
    ProposalResolution, 
    ApplicationReview,
    ProposalReview,
    ContractResolution,
    ContractReview,
    ContractCompletionFiles,
    ProjectCompletionFiles, 
    ProposalCompletionFiles 
)
from teams.models import Team


@login_required
def application_manager(request, application_id, project_slug):
    resolution = ''
    duration_end_time = ''
    application = get_object_or_404(ApplicationSale, pk=application_id, project__slug=project_slug)
    client_review = ApplicationReview.objects.filter(resolution__application=application)

    completion_form = ProjectCompletionForm(request.POST, request.FILES)
    if request.user.user_type == Customer.FREELANCER:
        if request.user != application.team.created_by:
            return redirect('transactions:application_transaction')

        project_resolution = ProjectResolution.objects.filter(
            application=application, 
            application__team__created_by = request.user, 
            application__team__pk=request.user.freelancer.active_team_id
        )
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
        if ProjectResolution.objects.filter(application=application, team=application.team).exists():
            print('%s' % (str('Application task already started')))
            pass
        else:
            try:
                ProjectResolution.start_new_project(
                    application=application, 
                    team=application.team
                )
            except Exception as e:
                print('%s' % (str(e))) 
           
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
        resolution = get_object_or_404(ProjectResolution, application=application, team=application.team)

        reviews = ApplicationReview.objects.filter(resolution=resolution, status=True)
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
                ProjectResolution.review_and_approve(
                    resolution_pk=resolution.pk, 
                    team=application.team, 
                    title=title, 
                    message=message, 
                    rating=rating
                )
                success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
            except Exception as e:
                error_messages = str(e)
                success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

        response = JsonResponse({'success_or_error_message': success_or_error_message})
        return response


@login_required
def proposal_manager(request, proposalsale_id, proposal_slug):
    resolution = ''
    duration_end_time = ''
    proposal_sold = get_object_or_404(ProposalSale, pk=proposalsale_id, proposal__slug=proposal_slug)
    client_review = ProposalReview.objects.filter(resolution__proposal_sale=proposal_sold)
    completion_form = ProposalCompletionForm(request.POST, request.FILES)
    
    if request.user.user_type == Customer.FREELANCER:
        if request.user != proposal_sold.team.created_by:
            return redirect('transactions:proposal_transaction') 

        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
        proposal_resolution = ProposalResolution.objects.filter(
            proposal_sale__pk=proposal_sold.id, 
            proposal_sale__team = team, 
            team=team
        )
        if proposal_resolution.count() > 0:
            resolution = proposal_resolution.first()
            duration_end_time = resolution.end_time

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

        proposal_sale = get_object_or_404(ProposalSale, pk=proposalsale_id, team__created_by=request.user, purchase__status = Purchase.SUCCESS)
        if ProposalResolution.objects.filter(proposal_sale=proposal_sale, team=proposal_sale.team).exists():
            print('%s' % (str('Proposal task already started'))) 
            pass
        else:
            try:
                ProposalResolution.start_new_proposal(
                    proposal_sale=proposal_sale, 
                    team=proposal_sale.team
                )
            except Exception as e:
                print('%s' % (str(e))) 
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
                ProposalResolution.review_and_approve(
                    resolution_pk=resolution.pk, 
                    team=proposal_sale.team, 
                    title=title, 
                    message=message, 
                    rating=rating
                )
                success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
            except Exception as e:
                error_messages = str(e)
                success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

        response = JsonResponse({'success_or_error_message': success_or_error_message})
        return response


@login_required
def contract_manager(request, contractsale_id, contract_slug):
    resolution = ''
    duration_end_time = ''
    contract_sold = get_object_or_404(ContractSale, pk=contractsale_id, contract__slug=contract_slug)
    client_review = ContractReview.objects.filter(resolution__contract_sale=contract_sold)
    completion_form = ContractCompletionForm(request.POST or None, request.FILES or None)
    
    if request.user.user_type == Customer.FREELANCER:
        if request.user != contract_sold.team.created_by:
            return redirect('transactions:contract_transaction') 

        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
        contract_resolution = ContractResolution.objects.filter(
            contract_sale__pk=contract_sold.id, 
            contract_sale__team = team, 
            team=team
        )
        if contract_resolution.count() > 0:
            resolution = contract_resolution.first()
            duration_end_time = resolution.end_time

    elif request.user.user_type == Customer.CLIENT:
        if request.user != contract_sold.purchase.client:
            return redirect('transactions:contract_transaction')        
        
        contract_resolution = ContractResolution.objects.filter(contract_sale=contract_sold, contract_sale__purchase__client = request.user)
        if contract_resolution.count() > 0:
            resolution = contract_resolution.first()
            duration_end_time = resolution.end_time  

    context = {
        "contract_sold": contract_sold,
        "client_review": client_review,
        "completion_form": completion_form,
        "duration_end_time": duration_end_time,
        "resolution": resolution,
        "currency": get_base_currency_code,
    }
    return render(request, "resolution/contract_resolution.html", context)


@login_required
@user_is_freelancer
def contract_start_work(request):
    if request.POST.get('action') == 'start-work':
        contractsale_id = int(request.POST.get('contractId'))

        contract_sale = get_object_or_404(ContractSale, pk=contractsale_id, team__created_by=request.user, purchase__status = Purchase.SUCCESS)
        if ContractResolution.objects.filter(contract_sale=contract_sale, team=contract_sale.team).exists():
            print('%s' % (str('Contract task already started'))) 
            pass
        else:
            try:
                ContractResolution.start_new_contract(
                    contract_sale=contract_sale, 
                    team=contract_sale.team
                )

            except Exception as e:
                print('%s' % (str(e)))            
        response = JsonResponse({'message': 'work started'})
        return response


login_required
@user_is_client
def contract_review(request):
    success_or_error_message = ''
    error_messages = ''
    if request.POST.get('action') == 'contract-review':
        contract_sold_id = int(request.POST.get('contractSoldId'))
        rating = int(request.POST.get('rating'))
        title = str(request.POST.get('title'))
        message = str(request.POST.get('message'))

        contract_sale = get_object_or_404(ContractSale, pk=contract_sold_id, purchase__client = request.user, purchase__status = Purchase.SUCCESS)
        resolution = get_object_or_404(ContractResolution, contract_sale=contract_sale, team=contract_sale.team)

        reviews = ContractReview.objects.filter(resolution=resolution, status=True)
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
                ContractResolution.review_and_approve(
                    resolution_pk=resolution.pk, 
                    team=contract_sale.team, 
                    title=title, 
                    message=message, 
                    rating=rating
                )
                success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
            except Exception as e:
                error_messages = str(e)
                success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

        response = JsonResponse({'success_or_error_message': success_or_error_message})
        return response






































