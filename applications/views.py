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
from transactions.models import Purchase, ApplicationSale, ProposalSale, ContractSale
from paypalcheckoutsdk.orders import OrdersGetRequest
from payments.paypal import PayPalClientConfig
from payments.stripe import StripeClientConfig
from general_settings.gateways import FlutterwaveClientConfig, RazorpayClientConfig
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
# from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.discount import get_discount_calculator, get_earning_calculator
from general_settings.fees_and_charges import get_application_fee_calculator
from django.db import transaction as db_transaction
from freelancer.models import FreelancerAccount
from teams.controller import PackageController
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
    can_apply_for_project = PackageController(team).monthly_projects_applicable_per_team()
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
    payment_gateways = request.merchant.merchant.gateways.all().exclude(name='balance')

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


# @login_required
# @user_is_client
# def application_fee_structure(request):
#     applicant_box = ApplicationAddon(request)
#     base_currency = get_base_currency_symbol()
#     if applicant_box.__len__() < 1:
#         messages.error(request, "Please add atleast one applicant to proceed")
#         return redirect("applications:application_multiple_summary")

#     payment_gateways = request.merchant.merchant.gateways.all().exclude(name='balance')
#     context = {
#         'applicant_box': applicant_box,
#         'base_currency': base_currency,
#         'payment_gateways': payment_gateways,
#     }
#     return render(request, "applications/application_fee_structure.html", context)


@login_required
@user_is_client
def application_fee(request):
    applicant_box = ApplicationAddon(request)

    if request.POST.get('action') == 'gateway':
        gateway_type = int(request.POST.get('gatewaytype'))
        gateway = PaymentGateway.objects.get(id=gateway_type)
        selected_fee = gateway.processing_fee
        applicants = applicant_box.__len__()
        discount = applicant_box.get_discount_value()
        subtotal = applicant_box.get_total_price_before_fee_and_discount()

        session = request.session

        if "applicationgateway" not in session:
            session["applicationgateway"] = {"gateway_id": gateway.id}
            session.modified = True
        else:
            session["applicationgateway"]["gateway_id"] = gateway.id
            session.modified = True

        context = {
            'selected_fee': selected_fee,
            'subtotal': subtotal,
            'discount': discount,
            'applicants': applicants,
        }
        response = JsonResponse(context)
        return response


@login_required
@user_is_client
def final_application_checkout(request):
    applicant_box = ApplicationAddon(request)
    
    if applicant_box.__len__() < 1:
        messages.error(request, "Please add atleast one applicant to proceed")
        return redirect("applications:application_multiple_summary")

    if "applicationgateway" not in request.session:
        messages.error(request, "Please select payment option")
        return redirect("applications:application_fee_structure")
    
    payment_data = calculate_payment_data(applicant_box)

    # Stripe payment api
    stripe_public_key = StripeClientConfig().stripe_public_key()
    # Paypal payment api
    paypal_public_key = PayPalClientConfig().paypal_public_key()
    # Futterwave payment api
    flutterwave_public_key = FlutterwaveClientConfig().flutterwave_public_key()
    # Razorpay payment api
    razorpay_public_key = RazorpayClientConfig().razorpay_public_key_id()

    currency = CurrencyForm()
    base_currency = get_base_currency(request)

    context = {
        'subtotal': payment_data.subtotal,
        'grand_total': payment_data.grand_total,
        'selected_fee': payment_data.total_gateway_fee,
        "gateway_type": payment_data.gateway_type,
        "paypal_public_key": paypal_public_key,
        "stripe_public_key": stripe_public_key,
        "flutterwave_public_key": flutterwave_public_key,
        "razorpay_public_key": razorpay_public_key,
        "currency": currency,
        "base_currency": base_currency,
    }
    return render(request, "applications/final_application_checkout.html", context)


@login_required
@user_is_client
def stripe_application_intent(request):
    applicant_box = ApplicationAddon(request)
    payment_data = calculate_payment_data(applicant_box)

    discount_value = applicant_box.get_discount_value()
    total_gateway_fee = applicant_box.get_fee_payable()
    grand_total_before_expense = applicant_box.get_total_price_before_fee_and_discount()
    grand_total = applicant_box.get_total_price_after_discount_and_fee()

    stripe_obj = StripeClientConfig()
    stripe_reference = stripe_obj.stripe_unique_reference()
    stripe.api_key = stripe_obj.stripe_secret_key()

    session = stripe.checkout.Session.create(
        metadata = {'mode':'payment'},
        payment_method_types=['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Hiring of Applicants',
                    },
                    'unit_amount': grand_total * 100,
                },
                'quantity': 1
            },
        ],
        mode='payment',
        success_url=f"{get_protocol_only()}{str(get_current_site(request))}/transaction/congrats/",
        cancel_url=f"{get_protocol_only()}{str(get_current_site(request))}/dashboard/",
    )
    gateway_type = str(applicant_box.get_gateway())
    payment_intent = session.payment_intent

    if Purchase.objects.filter(stripe_order_key=payment_intent).exists():
        pass
    else:
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                full_name=request.user.get_full_name,
                email=request.user.email,
                country=str(request.user.country),
                client_fee = int(total_gateway_fee),
                category = Purchase.PROJECT,
                payment_method=gateway_type,
                salary_paid=grand_total,
                unique_reference=stripe_reference,           
            )           
            purchase.stripe_order_key=payment_intent
            purchase.status=Purchase.FAILED
            purchase.save()
        except Exception as e:
            print('%s' % (str(e)))

        try:
            for applicant in applicant_box:
                ApplicationSale.objects.create(
                    team=applicant["application"].team,
                    purchase=purchase,
                    project=applicant["application"].project,
                    sales_price=int(applicant["budget"]),
                    staff_hired=int(1),
                    earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    total_earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    total_discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    disc_sales_price=int(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    total_sales_price=int((applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    earning=int(get_earning_calculator(
                        (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                        get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)))), 
                    total_earnings=int(get_earning_calculator(
                        (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                        get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))))             
                )
        except Exception as e:
            print('%s' % (str(e)))
        applicant_box.clean_box()
        return JsonResponse({'session': session, 'order': payment_intent})


@login_required
@user_is_client
def paypal_application_intent(request):
    applicant_box = ApplicationAddon(request)
    discount_value = applicant_box.get_discount_value()
    total_gateway_fee = applicant_box.get_fee_payable()
    gateway_type = applicant_box.get_gateway()
    grand_total_before_expense = applicant_box.get_total_price_before_fee_and_discount()

    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)
    data = body["orderID"]

    if data:
        paypal_request_order = OrdersGetRequest(data)
        response = PayPalClient.paypal_httpclient().execute(paypal_request_order)
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                full_name=response.result.purchase_units[0].shipping.name.full_name,
                email=response.result.payer.email_address,
                country=request.user.country,
                client_fee = int(total_gateway_fee), 
                category = Purchase.PROJECT,
                payment_method=str(gateway_type),
                salary_paid=round(float(response.result.purchase_units[0].amount.value)),
                paypal_order_key=response.result.id,
                unique_reference=PayPalClient.paypal_unique_reference(),
                status=Purchase.FAILED,
            )

        except Exception as e:
            print('%s' % (str(e)))
            
        try:
            for applicant in applicant_box:
                ApplicationSale.objects.create(
                    team=applicant["application"].team,
                    purchase=purchase,
                    project=applicant["application"].project,
                    sales_price=int(applicant["budget"]),
                    staff_hired=int(1),
                    earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    total_earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    total_discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    disc_sales_price=int(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    total_sales_price=int((applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    earning=int(get_earning_calculator(
                        (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                        get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)))), 
                    total_earnings=int(get_earning_calculator(
                        (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                        get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))))            
                )

        except Exception as e:
            print('%s' % (str(e)))

        try:
            Purchase.paypal_order_confirmation(pk=purchase.pk)
        except Exception as e:
            print('%s' % (str(e)))        

        applicant_box.clean_box()
        return JsonResponse({'Perfect': 'All was successful', })
    else:
        purchase.status = Purchase.FAILED
        purchase.save()
        return JsonResponse({'failed': 'Transaction failed, Razorpay will refund your money if you are already debited', })


@login_required
@user_is_client
def flutter_payment_intent(request):
    applicant_box = ApplicationAddon(request)
    discount_value = applicant_box.get_discount_value()
    total_gateway_fee = applicant_box.get_fee_payable()
    grand_total_before_expense = applicant_box.get_total_price_before_fee_and_discount()
    grand_total = applicant_box.get_total_price_after_discount_and_fee()
    base_currency = get_base_currency(request)

    flutterwaveClient = FlutterwaveClientConfig()
    tx_ref = flutterwaveClient.flutterwave_unique_reference()
    gateway_type = str(applicant_box.get_gateway())

    if Purchase.objects.filter(unique_reference=tx_ref).exists():
        pass
    else:
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                full_name=request.user.get_full_name,
                email=request.user.email,
                country=str(request.user.country),
                payment_method=gateway_type,
                client_fee = int(total_gateway_fee),
                category = Purchase.PROJECT,
                salary_paid=grand_total,
                unique_reference=tx_ref,           
            )           
            purchase.status=Purchase.FAILED
            purchase.save()
        except Exception as e:
            print('%s' % (str(e)))

        try:
            for applicant in applicant_box:
                ApplicationSale.objects.create(
                    team=applicant["application"].team,
                    purchase=purchase,
                    project=applicant["application"].project,
                    sales_price=int(applicant["budget"]),
                    staff_hired=int(1),
                    earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    total_earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    total_discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    disc_sales_price=int(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                    total_sales_price=int((applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    earning=int(get_earning_calculator(
                        (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                        get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)))), 
                    total_earnings=int(get_earning_calculator(
                        (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                        get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))))             
                )
        except Exception as e:
            print('%s' % (str(e)))

        redirect_url= f"{get_protocol_only()}{str(get_current_site(request))}/application/success/",
        auth_token = flutterwaveClient.flutterwave_secret_key()
        headers = {'Authorization': 'Bearer ' + auth_token}
        data = {
            "tx_ref": tx_ref,
            "amount": grand_total,
            "currency": base_currency,
            "redirect_url": redirect_url,
            "payment_options": "card, mobilemoneyghana, ussd",
            "meta": {
                "consumer_id": str(request.user.id),
            },
            "customer": {
                "email": str(request.user.email),
                "phonenumber": str(request.user.phone),
                "name": str(request.user)
            },
            "customizations": {
                "title": "Trosgate",
                "description": "Payment for applications",
                "logo": "", 
            }
        }
        # {{website.logo.url}}
        url = 'https://api.flutterwave.com/v3/payments'
        response = requests.post(url, json=data, headers=headers)
        response_to_json = response.json()
        redirectToCheckout = response_to_json['data']['link']

        return JsonResponse({'redirectToCheckout': redirectToCheckout, 'safe':False})


@login_required
@user_is_client
@require_http_methods(['GET', 'POST'])
def application_success(request):
    applicant_box = ApplicationAddon(request)
    status = request.GET.get('status', None)
    unique_reference = request.GET.get('tx_ref', '')
    flutterwave_order_key = request.GET.get('transaction_id', '')
    message = ''
    if status == 'successful' and unique_reference != '' and flutterwave_order_key != '':
        Purchase.flutterwave_order_confirmation(unique_reference=unique_reference, flutterwave_order_key=flutterwave_order_key)
        message = 'Payment succeeded'
    else:
        message = 'Payment failed'
        return HttpResponse(status=401)
       
    applicant_box.clean_box()
    context = {
        "good": message
    }
    return render(request, "applications/payment_success.html", context)


@login_required
@user_is_client
def razorpay_application_intent(request):
    applicant_box = ApplicationAddon(request)
    grand_total = applicant_box.get_total_price_after_discount_and_fee()
    gateway_type = applicant_box.get_gateway()
    base_currency = get_base_currency(request)
    discount_value = applicant_box.get_discount_value()
    total_gateway_fee = applicant_box.get_fee_payable()
    grand_total_before_expense = applicant_box.get_total_price_before_fee_and_discount()
    razorpay_api = RazorpayClientConfig()
    total_gateway_fee = applicant_box.get_fee_payable()
    unique_reference = razorpay_api.razorpay_unique_reference()
    
    try:
        purchase = Purchase.objects.create(
            client=request.user,
            full_name=f'{request.user.first_name} {request.user.last_name}',
            payment_method=str(gateway_type),
            category = Purchase.PROJECT,
            client_fee = int(total_gateway_fee),
            salary_paid=grand_total,
            unique_reference=unique_reference,
            status=Purchase.FAILED
        )
    except Exception as e:
        print('%s' % (str(e)))

    try:
        for applicant in applicant_box:
            ApplicationSale.objects.create(
                team=applicant["application"].team,
                purchase=purchase,
                project=applicant["application"].project,
                sales_price=int(applicant["budget"]),
                staff_hired=int(1),
                discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                total_discount_offered=int(get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                total_earning_fee_charged=int(get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                disc_sales_price=int(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)),
                total_sales_price=int((applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                earning=int(get_earning_calculator(
                    (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value)))), 
                total_earnings=int(get_earning_calculator(
                    (applicant["budget"] - (get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))),
                    get_application_fee_calculator(applicant["budget"] - get_discount_calculator(applicant["budget"], grand_total_before_expense, discount_value))))               
            )
    except Exception as e:
        print('%s' % (str(e)))
    notes = {'Total Price': 'The total amount may change with discount'}
    currency = base_currency
    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_order = razorpay_client.order.create(dict(
        amount=grand_total * 100,
        currency=currency,
        notes=notes,
        receipt=purchase.unique_reference
    ))
    print('razorpay_order', razorpay_order['id'])
    purchase.razorpay_order_key = razorpay_order['id']
    purchase.save()

    response = JsonResponse({'currency': currency, 'amount': (
        purchase.salary_paid), 'razorpay_order_key': purchase.razorpay_order_key})
    return response


@login_required
@user_is_client
def razorpay_webhook(request):
    applicant_box = ApplicationAddon(request)
    razorpay_client = RazorpayClientConfig().get_razorpay_client()
    application_items=''
    purchase_obj=''
    founder_account=''
    if request.POST.get('action') == 'razorpay-application':
        razorpay_order_key = str(request.POST.get('orderid'))
        razorpay_payment_id = str(request.POST.get('paymentid'))
        razorpay_signature = str(request.POST.get('signature'))

        data = {
            'razorpay_order_id': razorpay_order_key,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }


        signature = razorpay_client.utility.verify_payment_signature(data)

        if signature == True:
            try:
                Purchase.razorpay_order_confirmation(razorpay_order_key, razorpay_payment_id, razorpay_signature)
                applicant_box.clean_box()
                return JsonResponse({'Perfect':'All was successful',})
            except Exception as e:
                print('%s' % (str(e))) 

        else:
            return JsonResponse({'failed':'Transaction failed, Razorpay will refund your money if you are already debited',})
 


# @login_required
# @user_is_client
# def application_success(request):

#     context = {
#         "good": "All good"
#     }
#     return render(request, "applications/payment_success.html", context)

