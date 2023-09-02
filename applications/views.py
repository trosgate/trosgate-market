import requests
import base64
import json
import stripe
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import Project
from .models import Application
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from account.permission import user_is_freelancer, user_is_client
from account.models import Customer
from teams.models import Team
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime, timezone, timedelta
from . application import ApplicationAddon
from general_settings.models import Currency
from payments.models import PaymentGateway

from general_settings.forms import CurrencyForm
from django.views.decorators.csrf import csrf_exempt
from transactions.models import Purchase, ApplicationSale
from payments.paypal import PayPalClientConfig
from payments.stripe import StripeClientConfig
from payments.razorpay import RazorpayClientConfig
from payments.flutterwave import FlutterwaveClientConfig
from payments.paystack import PaystackClientConfig
from transactions.utilities import (
    get_base_currency, 
    calculate_payment_data, 
    PurchaseAndSaleCreator
)
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
from general_settings.discount import get_discount_calculator, get_earning_calculator
from general_settings.fees_and_charges import get_application_fee_calculator
from django.db import transaction as db_transaction
from freelancer.models import FreelancerAccount
from notification.mailer import application_notification
from general_settings.utilities import get_protocol_only
from analytics.analytic import user_review_rate
from transactions.utilities import get_base_currency, calculate_payment_data #, PurchaseAndSaleCreator


@login_required
@user_is_freelancer
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply_for_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, status=Project.ACTIVE)
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    can_apply_for_project = team.monthly_projects_slot
    print('can_apply_for_project ::', can_apply_for_project)
    applied = Application.objects.filter(team=team, project=project)
    base_currency = get_base_currency(request)

    if applied:
        messages.error(request, 'Your team already applied for this job!')

        return redirect("projects:project_detail", project_slug=project.slug)

    if request.method == 'POST':
        applyform = ApplicationForm(request.POST or None)

        if applyform.is_valid():
            application = applyform.save(commit=False)
            application.project = project
            application.team = team
            application.applied_by = request.user
            application.save()

            messages.info(request, 'Your application was created successfully!')
            try:
                application_notification(application)
            except:
                print('application mail not sent')

            return redirect(reverse("applications:freelancer_application"))

    else:
        applyform = ApplicationForm()

    context = {
        'applyform': applyform,
        'project': project,
        'base_currency': base_currency,
        'can_apply_for_project': can_apply_for_project
    }
    return render(request, 'applications/application.html', context)


@login_required
@user_is_client
def client_application_view(request):
    active_projects = Project.objects.filter(created_by=request.user, status=Project.ACTIVE)

    context = {
        'active_projects': active_projects,
    }
    return render(request, 'applications/client_application.html', context)


@login_required
@user_is_freelancer
def freelancer_application_view(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    applications = team.applications.filter(project__status=Project.ACTIVE)

    context = {
        'applications': applications,
    }
    return render(request, 'applications/freelancer_application.html', context)


@login_required
def application_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, status=Project.ACTIVE)
    base_currency = get_base_currency(request)
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
        applications = Application.objects.filter(project=project, team=team)
    elif request.user.user_type == Customer.CLIENT:
        applications = Application.objects.filter(project=project, project__created_by=request.user)

    context = {
        'project': project,
        'applications': applications,
        'base_currency': base_currency

    }
    return render(request, 'applications/manage_application_detail.html', context)


@login_required
def pricing_option_with_fees(request):
    applicant_box = ApplicationAddon(request)
    payment_gateways = request.merchant.gateways.all().exclude(name='balance')

    base_currency = get_base_currency(request)

    if request.method == 'POST':
        gateways = int(request.POST.get('paymentGateway'))
        gateway = PaymentGateway.objects.filter(id=gateways).first()

        session = request.session

        if gateway:
            if "applicationgateway" not in session:
                session["applicationgateway"] = {"gateway_id": gateway.id}
                session.modified = True
            else:
                session["applicationgateway"]["gateway_id"] = gateway.id
                session.modified = True
        else:
            pass
    payment_data = calculate_payment_data(applicant_box)

    context ={
        'applicant_box': applicant_box,
        'selected': 'selected',
        'payment_gateways': payment_gateways,
        'base_currency': base_currency,
        'payment_method': 'Payment Summary',
        "discount": payment_data['discount_value'],
        'subtotal': payment_data['grand_total_before_expense'],
        'grand_total': payment_data['grand_total'],
        'selected_fee': payment_data['total_gateway_fee'],
        "gateway_type": payment_data['gateway_type'],
    }
    if request.htmx:
        return render(request, "applications/partials/pricing_option_with_fees.html", context)

    return render(request, "applications/pricing_option_with_fees.html", context)


@login_required
@user_is_client
def add_or_remove_application(request):
    applicant_box = ApplicationAddon(request)
    project_id = int(request.POST.get('project'))
    application_id = int(request.POST.get('application'))

    project = get_object_or_404(Project, pk=project_id, created_by=request.user, status=Project.ACTIVE)
    application = get_object_or_404(Application, project=project, id=application_id)
    
    if application.accept == False:
        application.accept = True
        application.save()
        applicant_box.addon(application=application)

    else:
        application.accept = False
        application.save()
        applicant_box.remove(application=application_id) 

    applications = Application.objects.filter(project=project)
    context = {
        'applicant_box': applicant_box,
        'applications': applications,
    }
    return render(request, "applications/partials/accept_applicant.html", context)


@login_required
@user_is_client
def remove_application(request):
    applicant_box = ApplicationAddon(request)
    if request.POST.get('action') == 'post':
        application_id = int(request.POST.get('applicationid'))
        application = get_object_or_404(Application, id=application_id)
        application.accept = False
        application.save()        
        applicant_box.remove(application=application_id)
        freelancers = applicant_box.__len__()
        payment_data = calculate_payment_data(applicant_box)
        base_currency = get_base_currency(request)

        response = JsonResponse({
            'freelancers': freelancers,
            'base_currency':base_currency,
            'grandtotal': payment_data['grand_total'],
            'selected_fee': payment_data['total_gateway_fee'],
            "discount": payment_data['discount_value'],
        })
        return response


@login_required
@user_is_client
def final_application_checkout(request):
    applicant_box = ApplicationAddon(request)
    payment_data = calculate_payment_data(applicant_box)
    num_of_freelancers = applicant_box.__len__()

    if num_of_freelancers < 1:
        messages.error(request, "Please add atleast one applicant to proceed")
        return redirect("applications:pricing_option_with_fees")

    if  "applicationgateway" not in request.session:
        messages.error(request, "Please select payment option")
        return redirect("applications:pricing_option_with_fees")

    gateway_type = str(payment_data['gateway_type']).lower()

    base_currency = get_base_currency(request)
    paypal_public_key = ''
    stripeClient = ''
    razorpay_public_key = ''
    flutterwave_public_key = ''
    stripe_public_key = ''
    paystack_public_key = ''

    # Paypal payment api
    if gateway_type == 'paypal':
        paypal_public_key = PayPalClientConfig().paypal_public_key()

    # Stripe payment api
    elif gateway_type == 'stripe':
        stripeClient = StripeClientConfig()
        stripe_public_key = stripeClient.stripe_public_key()

    # Razorpay payment api
    elif gateway_type == 'razorpay':
        razorpay_public_key = RazorpayClientConfig().razorpay_key_id


    # Flutterwave payment api
    elif gateway_type == 'flutterwave':
        flutterwave_public_key = FlutterwaveClientConfig().flutterwave_public_key  
    
    # Paystack payment api
    elif gateway_type == 'paystack':
        paystack_public_key = PaystackClientConfig().paystack_public_key  


    context = {
        "discount": payment_data['discount_value'],
        'subtotal': payment_data['grand_total_before_expense'],
        'grand_total': payment_data['grand_total'],
        'selected_fee': payment_data['total_gateway_fee'],
        "gateway_type": gateway_type,
        "paystack_public_key": paystack_public_key,
        "paypal_public_key": paypal_public_key,
        "stripe_public_key": stripe_public_key,
        "flutterwave_public_key": flutterwave_public_key,
        "razorpay_public_key": razorpay_public_key,
        "currency": CurrencyForm(),
        "base_currency": base_currency,
    }

    return render(request, "applications/final_application_checkout.html", context)


@login_required
@user_is_client
def paystack_payment_intent(request):
    applicant_box = ApplicationAddon(request)
    payment_data = calculate_payment_data(applicant_box)
    purchase = None
    base_currency = get_base_currency(request)
    try:
        purchase = PurchaseAndSaleCreator()
        purchase.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.PROJECT,
            hiringbox=applicant_box,
        )
        response_data = {
            'reference': purchase.reference,
            'amount': (purchase.salary_paid * 100),
            'email': request.user.email,
            'currency': base_currency,
        }
        
        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'error': 'Error Occured'})


@csrf_exempt
def paystack_callback(request):
    applicant_box = ApplicationAddon(request)      
    payment_reference = request.POST.get('payment_reference')
    transaction_id = request.POST.get('transaction_reference')
    message = request.POST.get('message')
    status = request.POST.get('status')

    try:
        
        if status == 'success' and message == 'Approved':
            Purchase.paystack_order_confirmation(
                payment_reference, transaction_id
            )
            applicant_box.clean_box()
            return JsonResponse({
                'status': 'success', 
                'transaction_url': '/transaction/applications/'}
            )
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
  

@login_required
@user_is_client
def flutter_payment_intent(request):
    applicant_box = ApplicationAddon(request)
    payment_data = calculate_payment_data(applicant_box)
    purchase = None

    base_currency = get_base_currency(request)
    try:
        purchase = PurchaseAndSaleCreator()
        purchase.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.PROJECT,
            hiringbox=applicant_box,
        )
        response_data = {
            'tx_ref': purchase.reference, 
            'email':request.user.email,
            'phone':request.user.phone,
            'customer':request.user.get_full_name(),
            'amount': (purchase.salary_paid),
            'currency': base_currency,
        }

        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'error': 'Error Occured'})

    
@login_required
@require_http_methods(['GET'])
def flutter_success(request):
    applicant_box = ApplicationAddon(request)
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref', '')
    transaction_id = request.GET.get('transaction_id', '')

    flutterwave = FlutterwaveClientConfig()
    if status == 'successful' and tx_ref != '' and transaction_id != '':
        product = flutterwave.verify_payment(transaction_id)
        if product['status'] == 'success':

            Purchase.flutterwave_order_confirmation(
                reference=product['data']['tx_ref'], 
                flutterwave_transaction_id=product['data']['id']
            )

            applicant_box.clean_box()
            data = {"status": "success", 'redirect_url':'/application/flutter_success/'}
            return JsonResponse(data)
        else:
            data = {"status": 'failed'}
            return JsonResponse(data)
    else:
        data = {"status": 'failed'}
        return JsonResponse(data)


@login_required
@require_http_methods(['POST'])
def stripe_payment_intent(request):
    applicant_box = ApplicationAddon(request)
    payment_data = calculate_payment_data(applicant_box)
    grand_total = applicant_box.get_total_price_after_discount_and_fee()

    card_token = request.POST.get('card_token')
    stripe_client = StripeClientConfig()
    payment_id, client_secret = stripe_client.create_payment_intent(grand_total,card_token) 

    purchase = None
    try:
        purchase = PurchaseAndSaleCreator()
        purchase.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.PROJECT,
            stripe_order_key=payment_id,
            hiringbox=applicant_box,
        )
        response_data = {
            'client_secret': client_secret,
            'payment_intent': payment_id,
        }
        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'status': 'failed'})


@login_required
@require_http_methods(['POST'])
def stripe_payment_order(request):
    applicant_box = ApplicationAddon(request)
    stripe_order_key = request.POST.get('stripe_order_key')
    Purchase.stripe_order_confirmation(stripe_order_key)
    applicant_box.clean_box()
    transaction_url = reverse('transactions:application_transaction')
    return JsonResponse({'status': 'success', 'transaction_url':transaction_url})
    

@login_required
@require_http_methods(['GET'])
def paypal_payment_order(request):
    applicant_box = ApplicationAddon(request)
    grand_total = applicant_box.get_total_price_after_discount_and_fee()
    payment_data = calculate_payment_data(applicant_box)

    paypal_order_key = PayPalClientConfig().create_order(grand_total)
    if paypal_order_key:
        try:
            purchase = PurchaseAndSaleCreator()
            purchase.create_purchase_and_sales(
                client=request.user,
                **payment_data,
                category=Purchase.PROJECT,
                paypal_order_key=paypal_order_key,
                hiringbox=applicant_box,
            )
            response_data = {
                'paypal_order_key': paypal_order_key,
            }
            return JsonResponse(response_data)
        except Exception as e:
            print('purchase ID ::', str(e))
            return JsonResponse({'error': 'Invalid request method'})
    else:
        print('purchase ID ::', str(e))
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
@require_http_methods(['POST'])
def paypal_callback(request):
    applicant_box = ApplicationAddon(request)

    body = json.loads(request.body)
    paypal_order_key = body["paypal_order_key"]

    capture_data = PayPalClientConfig().capture_order(paypal_order_key)
    capture_data_id = capture_data['purchase_units'][0]['payments']['captures'][0]['id']
    
    if capture_data['status'] == 'COMPLETED':
        Purchase.paypal_order_confirmation(paypal_order_key, capture_data_id)
        applicant_box.clean_box()
        return JsonResponse(capture_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@login_required
@user_is_client
def razorpay_application_intent(request):
    applicant_box = ApplicationAddon(request)
    grand_total = applicant_box.get_total_price_after_discount_and_fee()
    payment_data = calculate_payment_data(applicant_box)
    purchase = None
    base_currency = get_base_currency(request)

    razorpay_order_key = RazorpayClientConfig().create_order(grand_total)
    if razorpay_order_key:
        try:
            creator = PurchaseAndSaleCreator()
            purchase = creator.create_purchase_and_sales(
                client=request.user,
                **payment_data,
                category=Purchase.PROJECT,
                razorpay_order_key=razorpay_order_key,
                hiringbox=applicant_box,
            )

            response_data = {
                'razorpay_order_key': razorpay_order_key,
                'currency': base_currency,
                'amount': purchase.salary_paid,
                'razorpay_order_key': purchase.razorpay_order_key,
            }
            print('purchase ID ::', purchase.id)
            return JsonResponse(response_data)
        except Exception as e:
            print('purchase ID ::', str(e))
            return JsonResponse({'error': 'Invalid request method'})
    else:
        print('purchase ID ::', str(e))
        return JsonResponse({'error': 'Invalid request method'})


@login_required
@user_is_client
def razorpay_callback(request):
    applicant_box = ApplicationAddon(request)      
    razorpay_client = RazorpayClientConfig().razorpay
 
    razorpay_order_key = request.POST.get('orderid')
    razorpay_payment_id = request.POST.get('paymentid')
    razorpay_signature = request.POST.get('signature')
    
    data ={
        'razorpay_order_id': razorpay_order_key,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    signature = razorpay_client.utility.verify_payment_signature(data)

    if signature == True:
        try:
            Purchase.razorpay_order_confirmation(razorpay_order_key, razorpay_payment_id, razorpay_signature)
            applicant_box.clean_box()
            return JsonResponse({'status':'success','transaction_url':'/transaction/applications/'})
        except Exception as e:
            print('%s' % (str(e)))
            return JsonResponse({'status':'error'}) 

    else:
        return JsonResponse({'status':'error'})
 
        