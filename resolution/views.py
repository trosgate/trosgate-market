from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from contract.models import InternalContract
from projects.models import Project
from applications.models import Application
from proposals.models import Proposal
from account.models import Customer
from django.http import JsonResponse
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from account.permission import user_is_freelancer, user_is_client
from django.http import HttpResponse, HttpResponseBadRequest
from django_htmx.http import HttpResponseClientRedirect
from django.utils import timezone
from account.fund_exception import ReviewException
from . forms import (
#     ProjectCompletionForm, 
#     ProposalCompletionForm, 
#     ContractCompletionForm,
#     ApplicationCancellationForm,
    ProposalCancellationForm,
#     ContractCancellationForm,
)
from transactions.models import (
    Purchase, 
    ProposalSale, 
    ContractSale,
    ApplicationSale 
)
from . models import (
    ProposalJob,
    # ProjectResolution,
    # ApplicationReview,
    # ProposalReview,
    # ContractResolution,
    # ContractReview,
    # ApplicationCancellation,
    # ProposalCancellation,
    # ContractCancellation,
    # ProjectCompletionFiles, 
)
from teams.models import Team





@login_required
def proposal_manager(request, product_id, product_slug):
    product = get_object_or_404(ProposalSale, pk=product_id, proposal__slug=product_slug)
    if not (product.team.created_by == request.user or product.purchase.client == request.user):
        return HttpResponseBadRequest()
    cancellation_form = ProposalCancellationForm(request.POST or None)
    task = ProposalJob.objects.filter(product=product).first()
    print('Task ::', task)
    print('product ::', product)
    context = {
        "product": product,
        "task": task,
        "duration_end_time": product.end_time,
        "currency": get_base_currency_code,
        # "client_review": client_review,
        # "completion_form": completion_form,
        "cancellation_form": cancellation_form,
        # "cancellation_message": cancellation_message,        
    }
    return render(request, "resolution/proposal_job.html", context)



@login_required
@user_is_freelancer
def proposal_start_work(request):
    pk = int(request.GET.get('product'))
    product = get_object_or_404(
        ProposalSale, pk=pk, 
        team__created_by=request.user, 
        purchase__status = Purchase.SUCCESS
    )

    task, product_ = ProposalSale.start_task(product.id)
    url = product.get_absolute_url()

    if product.status == ProposalSale.ONGOING:
        messages.info(request, "Task Started successfully") 
        return HttpResponseClientRedirect(url)
    
    if product_.status == ProposalSale.ONGOING:
        messages.info(request, "Task Started successfully") 
        return HttpResponseClientRedirect(url)
    
    context ={'variable': 'taskStopped', 'task':task, 'product':product_}
    return render(request, 'resolution/component/task_started.html', context)


login_required
@user_is_client
def proposal_review(request):
    pass
#     success_or_error_message = ''
#     error_messages = ''
#     if request.POST.get('action') == 'proposal-review':
#         proposal_sold_id = int(request.POST.get('proposalSoldId'))
#         rating = int(request.POST.get('rating'))
#         title = str(request.POST.get('title'))
#         message = str(request.POST.get('message'))

#         proposal_sale = get_object_or_404(ProposalSale, pk=proposal_sold_id, purchase__client = request.user, purchase__status = Purchase.SUCCESS)
#         resolution = get_object_or_404(ProposalResolution, proposal_sale=proposal_sale, team=proposal_sale.team)

#         reviews = ProposalReview.objects.filter(resolution=resolution, status=True)
#         if reviews.count() > 0:
#             review = reviews.first()
#             review.resolution = resolution
#             review.title = title
#             review.message = message
#             review.rating = rating
#             review.status = True
#             review.save()
#             success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review modified Successfully</span>'
#         else:
#             try:
#                 ProposalResolution.review_and_approve(
#                     resolution_pk=resolution.pk, 
#                     team=proposal_sale.team, 
#                     title=title, 
#                     message=message, 
#                     rating=rating
#                 )
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
#             except Exception as e:
#                 error_messages = str(e)
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

#         response = JsonResponse({'success_or_error_message': success_or_error_message})
#         return response


# @login_required
# @user_is_client
# def proposal_cancelled(request):
#     resolution_id = request.POST.get('resolution')
#     cancel_type = request.POST.get('cancel_type', '')
#     message = request.POST.get('message', '')
#     cancellation_message = None
#     resolution = get_object_or_404(ProposalResolution, pk=resolution_id, status = 'ongoing', proposal_sale__purchase__client = request.user)
    
#     message_length = len(message) <= 500
#     if cancel_type != '' and message != '' and message_length:
#         if ProposalCancellation.objects.filter(resolution=resolution).exists():
#             pass
#         else:
#             try:
#                 ProposalResolution.cancel_proposal(
#                     resolution=resolution.id, 
#                     cancel_type=cancel_type,
#                     message=message
#                 )
                
#             except Exception as e:
#                 print(str(e))

#     cancel_message = ProposalCancellation.objects.filter(resolution=resolution, status = 'initiated')
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()
#     messages.info(request, "Cancellation initiated")    
#     context = {
#         'cancellation_message':cancellation_message
#     }       
#     return render(request, 'resolution/component/proposal_cancelled.html', context)


# @login_required
# @user_is_freelancer
# def confirm_proposal_cancel(request):
#     resolution_id = request.POST.get('confirmcancelproposal')
#     resolution = get_object_or_404(ProposalResolution, pk=resolution_id, proposal_sale__team__created_by = request.user)    
    
#     try:
#         ProposalResolution.approve_and_cancel_proposal(resolution=resolution.id)
#         return HttpResponse("<div style='color:green;'> Successfully cancelled order</div>")
#     except Exception as e:
#         errors = (str(e))
#         return HttpResponse(f"<div style='color:red;'> {errors} </div>")    



# @login_required
# def application_manager(request, application_id, project_slug):
#     resolution = None
#     duration_end_time = ''
#     cancellation_message = None
#     application = get_object_or_404(ApplicationSale, pk=application_id, project__slug=project_slug)
#     # client_review = ApplicationReview.objects.filter(resolution__application=application)

#     completion_form = ProjectCompletionForm(request.POST or None, request.FILES or None)
#     cancellation_form = ApplicationCancellationForm(request.POST or None)
        
#     if request.user.user_type == Customer.FREELANCER:

#         # project_resolution = ProjectResolution.objects.filter(
#         #     application=application, 
#         #     application__team__created_by = request.user, 
#         #     application__team__pk=request.user.freelancer.active_team_id
#         # )
#         if project_resolution.count() > 0:
#             resolution = project_resolution.first()
#             duration_end_time = resolution.end_time
            
#         if resolution and completion_form.is_valid():
#             completed_file = completion_form.save(commit=False)
#             completed_file.application = resolution
#             completed_file.save()

#     elif request.user.user_type == Customer.CLIENT:       
        
#         project_resolution = ProjectResolution.objects.filter(application=application, application__purchase__client = request.user)
#         if project_resolution.count() > 0:
#             resolution = project_resolution.first()
#             duration_end_time = resolution.end_time            
    
#     cancel_message = ApplicationCancellation.objects.filter(resolution=resolution)
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()

#     context = {
#         "application": application,
#         "client_review": client_review,
#         "completion_form": completion_form,
#         "duration_end_time": duration_end_time,
#         "cancellation_form": cancellation_form,
#         "cancellation_message": cancellation_message,
#         "resolution": resolution,
#         "currency": get_base_currency_code,

#     }
#     return render(request, "resolution/application_resolution.html", context)


# @login_required
# @user_is_client
# def application_cancelled(request):
#     resolution_id = request.POST.get('resolution')
#     cancel_type = request.POST.get('cancel_type', '')
#     message = request.POST.get('message', '')
#     cancellation_message = None

#     resolution = get_object_or_404(ProjectResolution, pk=resolution_id, status = 'ongoing', application__purchase__client = request.user)
    
#     message_length = len(message) <= 500
#     if cancel_type != '' and message != '' and message_length:
#         if ApplicationCancellation.objects.filter(resolution=resolution).exists():
#             pass
#         else:
#             try:
#                 ProjectResolution.cancel_project(
#                     resolution=resolution.id, 
#                     cancel_type=cancel_type,
#                     message=message
#                 )
#             except Exception as e:
#                 print(str(e))

#     cancel_message = ApplicationCancellation.objects.filter(resolution=resolution, status = 'initiated')
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()    
#     context = {
#         'cancellation_message':cancellation_message
#     }
#     return render(request, 'resolution/component/application_cancelled.html', context)


# @login_required
# @user_is_freelancer
# def confirm_application_cancel(request):
#     resolution_id = request.POST.get('confirm_cancel')
#     resolution = get_object_or_404(ProjectResolution, pk=resolution_id, application__team__created_by = request.user)    
#     try:
#         ProjectResolution.approve_and_cancel_project(resolution=resolution.id)
#         return HttpResponse("<div style='color:green;'> Successfully approved cancellation request </div>")
#     except Exception as e:
#         errors = (str(e))
#         return HttpResponse(f"<div style='color:red;'> {errors} </div>")    


# @login_required
# @user_is_freelancer
# def applicant_start_work(request):
#     if request.POST.get('action') == 'start-work':
#         applicationsale_id = int(request.POST.get('applicationid'))

#         application = get_object_or_404(ApplicationSale, pk=applicationsale_id, team__created_by=request.user, purchase__status = Purchase.SUCCESS)
#         if ProjectResolution.objects.filter(application=application, team=application.team).exists():
#             print('%s' % (str('Application task already started')))
#             pass
#         else:
#             try:
#                 ProjectResolution.start_new_project(
#                     application=application, 
#                     team=application.team
#                 )
#             except Exception as e:
#                 print('%s' % (str(e))) 
           
#         response = JsonResponse({'message': 'work started'})
#         return response


# @login_required
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
#         resolution = get_object_or_404(ProjectResolution, application=application, team=application.team)

#         reviews = ApplicationReview.objects.filter(resolution=resolution, status=True)
#         if reviews.count() > 0:
#             review = reviews.first()
#             review.resolution = resolution
#             review.title = title
#             review.message = message
#             review.rating = rating
#             review.status = True
#             review.save()
#             success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review modified Successfully</span>'
#         else:
#             try:
#                 ProjectResolution.review_and_approve(
#                     resolution_pk=resolution.pk, 
#                     team=application.team, 
#                     title=title, 
#                     message=message, 
#                     rating=rating
#                 )
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
#             except Exception as e:
#                 error_messages = str(e)
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

#         response = JsonResponse({'success_or_error_message': success_or_error_message})
#         return response


# @login_required
# def contract_manager(request, contractsale_id, contract_slug):
#     resolution = None
#     duration_end_time = ''
#     cancellation_message = None
#     contract_sold = get_object_or_404(ContractSale, pk=contractsale_id, contract__slug=contract_slug)
#     client_review = ContractReview.objects.filter(resolution__contract_sale=contract_sold)
#     completion_form = ContractCompletionForm(request.POST or None, request.FILES or None)
#     cancellation_form = ContractCancellationForm(request.POST or None)
#     if request.user.user_type == Customer.FREELANCER:
        
#         team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
#         contract_resolution = ContractResolution.objects.filter(
#             contract_sale__pk=contract_sold.id,
#             team=team
#         )
#         if contract_resolution.count() > 0:
#             resolution = contract_resolution.first()
#             duration_end_time = resolution.end_time

#     elif request.user.user_type == Customer.CLIENT:
        
#         contract_resolution = ContractResolution.objects.filter(contract_sale=contract_sold, contract_sale__purchase__client = request.user)
#         if contract_resolution.count() > 0:
#             resolution = contract_resolution.first()
#             duration_end_time = resolution.end_time  

#     cancel_message = ContractCancellation.objects.filter(resolution=resolution)
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()

#     context = {
#         "contract_sold": contract_sold,
#         "cancellation_form": cancellation_form,
#         "cancellation_message": cancellation_message,
#         "client_review": client_review,
#         "completion_form": completion_form,
#         "duration_end_time": duration_end_time,
#         "resolution": resolution,
#         "currency": get_base_currency_code,
#     }
#     return render(request, "resolution/contract_resolution.html", context)


# @login_required
# @user_is_freelancer
# def contract_start_work(request):
#     if request.POST.get('action') == 'start-work':
#         contractsale_id = int(request.POST.get('contractId'))

#         contract_sale = get_object_or_404(ContractSale, pk=contractsale_id, team__created_by=request.user, purchase__status = Purchase.SUCCESS)
#         if ContractResolution.objects.filter(contract_sale=contract_sale, team=contract_sale.team).exists():
#             print('%s' % (str('Contract task already started'))) 
#             pass
#         else:
#             try:
#                 ContractResolution.start_new_contract(
#                     contract_sale=contract_sale, 
#                     team=contract_sale.team
#                 )

#             except Exception as e:
#                 print('%s' % (str(e)))            
#         response = JsonResponse({'message': 'work started'})
#         return response


# login_required
# @user_is_client
# def contract_review(request):
#     success_or_error_message = ''
#     error_messages = ''
#     if request.POST.get('action') == 'contract-review':
#         contract_sold_id = int(request.POST.get('contractSoldId'))
#         rating = int(request.POST.get('rating'))
#         title = str(request.POST.get('title'))
#         message = str(request.POST.get('message'))

#         contract_sale = get_object_or_404(ContractSale, pk=contract_sold_id, purchase__client = request.user, purchase__status = Purchase.SUCCESS)
#         resolution = get_object_or_404(ContractResolution, contract_sale=contract_sale, team=contract_sale.team)

#         reviews = ContractReview.objects.filter(resolution=resolution, status=True)
#         if reviews.count() > 0:
#             review = reviews.first()
#             review.resolution = resolution
#             review.title = title
#             review.message = message
#             review.rating = rating
#             review.status = True
#             review.save()
#             success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review modified Successfully</span>'
#         else:
#             try:
#                 ContractResolution.review_and_approve(
#                     resolution_pk=resolution.pk, 
#                     team=contract_sale.team, 
#                     title=title, 
#                     message=message, 
#                     rating=rating
#                 )
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
#             except Exception as e:
#                 error_messages = str(e)
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

#         response = JsonResponse({'success_or_error_message': success_or_error_message})
#         return response


# @login_required
# @user_is_client
# def internal_contract_cancelled(request):
#     resolution_id = request.POST.get('resolution')
#     cancel_type = request.POST.get('cancel_type', '')
#     message = request.POST.get('message', '')
#     cancellation_message = None
#     resolution = get_object_or_404(ContractResolution, pk=resolution_id, status = 'ongoing', contract_sale__purchase__client = request.user)
    
#     message_length = len(message) <= 500
#     if cancel_type != '' and message != '' and message_length:
#         if ContractCancellation.objects.filter(resolution=resolution).exists():
#             pass
#         else:
#             try:
#                 ContractResolution.cancel_internal_contract(
#                     resolution=resolution.id, cancel_type=cancel_type,message=message
#                 )
#             except Exception as e:
#                 print(str(e))

#     cancel_message = ContractCancellation.objects.filter(resolution=resolution, status = 'initiated')
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()    
#     context = {
#         'cancellation_message':cancellation_message
#     }       
#     return render(request, 'resolution/component/contract_cancelled.html', context)


# @login_required
# @user_is_freelancer
# def confirm_internal_contract(request):
#     resolution_id = request.POST.get('confirmcancelcontract')
#     resolution = get_object_or_404(ContractResolution, pk=resolution_id, contract_sale__team__created_by = request.user)    
#     try:
#         ContractResolution.approve_and_cancel_internal_contract(resolution=resolution.id)
#         return HttpResponse("<div style='color:green;'> Successfully approved cancellation request </div>")
#     except Exception as e:
#         errors = (str(e))
#         return HttpResponse(f"<div style='color:red;'> {errors} </div>")    


# @login_required
# def oneclick_manager(request, purchase_pk, reference):
#     resolution = None
#     duration_end_time = ''
#     oneclick_resolution=None
#     cancellation_message = None

#     oneclick_sold = get_object_or_404(OneClickPurchase, pk=purchase_pk, reference=reference)

#     client_review = OneClickReview.objects.filter(resolution__oneclick_sale=oneclick_sold)
#     # completion_form = OneClickCompletionForm(request.POST or None, request.FILES or None)
#     cancellation_form = OneClickCancellationForm(request.POST or None)
#     if request.user.user_type == Customer.FREELANCER:
#         if request.user != oneclick_sold.team.created_by:
#             return redirect('transactions:one_click_transaction')

#         team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
#         oneclick_resolution = OneClickResolution.objects.filter(oneclick_sale=oneclick_sold, oneclick_sale__team=team)
#         if oneclick_resolution.count() > 0:
#             resolution = oneclick_resolution.first()
#             duration_end_time = resolution.end_time


#     elif request.user.user_type == Customer.CLIENT:
#         if request.user != oneclick_sold.client:
#             return redirect('transactions:one_click_transaction')

#         oneclick_resolution = OneClickResolution.objects.filter(oneclick_sale=oneclick_sold, oneclick_sale__client=request.user)
#         if oneclick_resolution.count() > 0:
#             resolution = oneclick_resolution.first()
#             duration_end_time = resolution.end_time

#     cancel_message = OneClickCancellation.objects.filter(resolution=resolution)
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()

#     context = {
#         "oneclick_sold": oneclick_sold,
#         "resolution": resolution,
#         # "completion_form": completion_form,
#         "cancellation_form": cancellation_form,
#         "cancellation_message": cancellation_message,        
#         "client_review": client_review,
#         "duration_end_time": duration_end_time,
#         "currency": get_base_currency_code,
#     }
#     return render(request, "resolution/oneclick_resolution.html", context)


# @login_required
# @user_is_freelancer
# def oneclick_start_work(request):
#     if request.POST.get('action') == 'start-work':
#         oneclick_id = int(request.POST.get('oneclickId'))

#         oneclick_sale = get_object_or_404(OneClickPurchase, pk=oneclick_id, team__created_by=request.user, status = OneClickPurchase.SUCCESS)
#         if OneClickResolution.objects.filter(oneclick_sale=oneclick_sale, team=oneclick_sale.team).exists():
#             print('%s' % (str('Oneclick task already started'))) 
#             pass
#         else:
#             try:
#                 OneClickResolution.start_oneclick(oneclick_sale=oneclick_sale,team=oneclick_sale.team)
#             except Exception as e:
#                 print('%s' % (str(e)))            
#         response = JsonResponse({'message': 'work started'})
#         return response


# login_required
# @user_is_client
# def oneclick_review(request):
#     success_or_error_message = ''
#     error_messages = ''
#     reviews=''
#     resolution=''
#     if request.POST.get('action') == 'oneclick-review':
#         oneclick_id = int(request.POST.get('oneclickId'))
#         rating = int(request.POST.get('rating'))
#         title = str(request.POST.get('title'))
#         message = str(request.POST.get('message'))

#         oneclick_sale = get_object_or_404(OneClickPurchase, pk=oneclick_id, client=request.user, status = OneClickPurchase.SUCCESS)
#         resolution = get_object_or_404(OneClickResolution, oneclick_sale=oneclick_sale, team=oneclick_sale.team)

#         reviews = OneClickReview.objects.filter(resolution=resolution, status=True)
#         if reviews.count() > 0:
#             review = reviews.first()
#             review.resolution = resolution
#             review.title = title
#             review.message = message
#             review.rating = rating
#             review.status = True
#             review.save()
#             success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review modified Successfully</span>'
#         else:
#             try:
#                 OneClickResolution.review_and_approve(
#                     resolution_pk=resolution.pk, 
#                     team=oneclick_sale.team, 
#                     title=title, 
#                     message=message, 
#                     rating=rating
#                 )
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:green;"> Review received Successfully</span>'
#             except Exception as e:
#                 error_messages = str(e)
#                 success_or_error_message = f'<span id="reviewerror-message" style="color:red;"> {error_messages}</span>'

#             response = JsonResponse({'success_or_error_message': success_or_error_message})
#             return response


# @login_required
# @user_is_client
# def oneclick_cancelled(request):
#     resolution_id = request.POST.get('resolution')
#     cancel_type = request.POST.get('cancel_type', '')
#     message = request.POST.get('message', '')
#     cancellation_message = None
#     resolution = get_object_or_404(OneClickResolution, pk=resolution_id, status = 'ongoing', oneclick_sale__client = request.user)
    
#     message_length = len(message) <= 500
#     if cancel_type != '' and message != '' and message_length:
#         if OneClickCancellation.objects.filter(resolution=resolution).exists():
#             pass
#         else:
#             try:
#                 OneClickResolution.cancel_oneclick(
#                     resolution=resolution.id, cancel_type=cancel_type,message=message
#                 )
#             except Exception as e:
#                 print(str(e))

#     cancel_message = OneClickCancellation.objects.filter(resolution=resolution, status = 'initiated')
#     if cancel_message.count() > 0:
#         cancellation_message = cancel_message.first()    
#     context = {
#         'cancellation_message':cancellation_message
#     }       
#     return render(request, 'resolution/component/oneclick_cancelled.html', context)


# @login_required
# @user_is_freelancer
# def confirm_oneclick_contract(request):
#     resolution_id = request.POST.get('confirmcanceloneclick')
#     resolution = get_object_or_404(OneClickResolution, pk=resolution_id, oneclick_sale__team__created_by = request.user)    
#     try:
#         OneClickResolution.approve_and_cancel_oneclick(resolution=resolution.id)
#         return HttpResponse("<div style='color:green;'> Successfully approved cancellation request </div>")
#     except Exception as e:
#         errors = (str(e))
#         return HttpResponse(f"<div style='color:red;'> {errors} </div>")    


# @login_required
# def remove_message(request):
#     return HttpResponse('')






























