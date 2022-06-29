import stripe
import random
import json
import math
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import Project
from applications.models import Application
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.utils.text import slugify
from client.models import Client
from account.permission import user_is_freelancer, user_is_client
from account.models import Customer
from teams.models import Team, Package
from proposals.models import Proposal
from paypalcheckoutsdk.orders import OrdersGetRequest
from general_settings.models import PaymentGateway
from general_settings.gateways import PayPalClientConfig, StripeClientConfig, FlutterwaveClientConfig, RazorpayClientConfig
from django.views.decorators.csrf import csrf_exempt
from .models import ApplicationSale, Purchase, ProposalSale, ContractSale, SalesReporting, SubscriptionItem
from . forms import PurchaseForm
from .hiringbox import HiringBox
from general_settings.fees_and_charges import get_proposal_fee_calculator
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.discount import get_discount_calculator, get_earning_calculator
from general_settings.forms import CurrencyForm
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods
from contract.models import InternalContract
from django.utils import timezone
from datetime import timedelta


def get_expiration():
    return (timezone.now() + timedelta(days = 30))


@login_required
def proposal_single_summary(request, short_name, proposal_slug):
    proposal = get_object_or_404(
        Proposal, created_by__short_name=short_name,  slug=proposal_slug)
    payments = PaymentGateway.objects.filter(status=True)

    context = {
        'proposal': proposal,
        'payments': payments,
    }
    return render(request, "transactions/proposal_single_summary.html", context)


@login_required
def proposal_multiple_summary(request):
    hiringbox = HiringBox(request)
    payments = PaymentGateway.objects.filter(status=True)
    return render(request, "transactions/proposal_multiple_summary.html", {'hiringbox': hiringbox, 'payments': payments})


@login_required
def add_proposal_to_box(request):
    hiringbox = HiringBox(request)

    if request.POST.get('action') == 'post':
        proposal_id = int(request.POST.get('proposalid'))
        member_qty = int(request.POST.get('memberqty'))
        proposal = get_object_or_404(
            Proposal, id=proposal_id, status=Proposal.ACTIVE)

        hiringbox.addon(proposal=proposal, member_qty=member_qty)
        memberqty = hiringbox.__len__()
        totals = hiringbox.get_total_price_before_fee_and_discount()

        response = JsonResponse(
            {'salary': proposal.salary, 'member_qty': memberqty, 'get_totals': totals})
        return response


@login_required
def remove_from_hiring_box(request):
    hiringbox = HiringBox(request)
    if request.POST.get('action') == 'post':
        proposal_id = int(request.POST.get('proposalid'))
        hiringbox.remove(proposal=proposal_id)
        memberqty = hiringbox.__len__()
        grand_total = hiringbox.get_total_price_before_fee_and_discount()
        response = JsonResponse(
            {'member_qty': memberqty, 'grandtotal': grand_total})
        return response


@login_required
def modify_from_hiring_box(request):
    hiringbox = HiringBox(request)
    if request.POST.get('action') == 'post':
        proposal_id = int(request.POST.get('proposalid'))
        member_qty = int(request.POST.get('memberqty'))
        hiringbox.modify(proposal=proposal_id, member_qty=member_qty)
        proposal = get_object_or_404(Proposal, id=proposal_id, status=Proposal.ACTIVE)

        line_total_price = member_qty * proposal.salary
        memberqty = hiringbox.__len__()
        grand_total = hiringbox.get_total_price_before_fee_and_discount()
        response = JsonResponse({'member_qty': memberqty, 'grandtotal': grand_total, 'total_price': line_total_price})
        return response


@login_required
def payment_option_with_fees(request):
    hiringbox = HiringBox(request)

    if hiringbox.__len__() < 1:
        messages.error(request, "Please add atleast one proposal to proceed")
        return redirect("transactions:hiring_box_summary")

    payment_gateways = PaymentGateway.objects.filter(status=True)
    base_currency = get_base_currency_symbol()    
    context ={
        'hiringbox': hiringbox,
        'payment_gateways': payment_gateways,
        'base_currency': base_currency
    }
    return render(request, "transactions/payment_option_with_fees.html", context)


@login_required
def payment_fee_structure(request):
    hiringbox = HiringBox(request)
    if request.POST.get('action') == 'post':
        gateway_type = int(request.POST.get('gatewaytype'))
        gateway = PaymentGateway.objects.get(id=gateway_type)
        selected_fee = gateway.processing_fee
        applicants = hiringbox.__len__()
        discount = hiringbox.get_discount_value()
        subtotal = hiringbox.get_total_price_before_fee_and_discount()

        session = request.session

        if "proposalgateway" not in request.session:
            session["proposalgateway"] = {"gateway_id": gateway.id}
            session.modified = True
        else:
            session["proposalgateway"]["gateway_id"] = gateway.id
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
def final_checkout(request):
    hiringbox = HiringBox(request)
    num_of_freelancers = hiringbox.__len__()

    if num_of_freelancers < 1:
        messages.error(request, "Please add atleast one proposal to proceed")
        return redirect("transactions:hiring_box_summary")

    if  "proposalgateway" not in request.session:
        messages.error(request, "Please select payment option")
        return redirect("transactions:payment_option_selection")

    gateway_type = hiringbox.get_gateway()
    selected_fee = hiringbox.get_fee_payable()
    subtotal = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    base_currency = get_base_currency_code()
    total_after_discount = hiringbox.get_total_price_after_discount_only()

    # Stripe payment api
    stripeClient = StripeClientConfig()
    stripe_public_key = stripeClient.stripe_public_key()
    stripe.api_key = stripeClient.stripe_secret_key()
    # Paypal payment api
    paypal_public_key = PayPalClientConfig().paypal_public_key()   
    # Futterwave payment api
    flutterwave_public_key = FlutterwaveClientConfig().flutterwave_public_key()  
    # Razorpay payment api
    razorpay_public_key = RazorpayClientConfig().razorpay_public_key_id()

    currency = CurrencyForm()

    context = {
        'subtotal': subtotal,
        'grand_total': grand_total,
        'selected_fee': selected_fee,
        "gateway_type": gateway_type,
        "paypal_public_key": paypal_public_key,
        "stripe_public_key": stripe_public_key,
        "flutterwave_public_key": flutterwave_public_key,
        "razorpay_public_key": razorpay_public_key,
        "currency": currency,
        "base_currency": base_currency,
    }

    return render(request, "transactions/final_proposal_checkout.html", context)


@login_required
@user_is_client
def flutter_payment_intent(request):
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    gateway_type = str(hiringbox.get_gateway())
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    number_of_applicants = hiringbox.__len__()
    shared_gateway_fee = total_gateway_fee/number_of_applicants
    grand_total = hiringbox.get_total_price_after_discount_and_fee()

    shared_gateway_fee = total_gateway_fee/number_of_applicants
    base_currency = get_base_currency_code()

    flutterwaveClient = FlutterwaveClientConfig()
    unique_reference = flutterwaveClient.flutterwave_unique_reference()


    if Purchase.objects.filter(unique_reference=unique_reference).exists():
        pass
    else:
        purchase = Purchase.objects.create(
            client=request.user,
            full_name=request.user.get_full_name,
            email=request.user.email,
            country=str(request.user.country),
            payment_method=gateway_type,
            salary_paid=grand_total,
            unique_reference=unique_reference,           
        )           

        purchase.status=Purchase.FAILED
        purchase.save()

        for proposal in hiringbox:
            ProposalSale.objects.create(
                team=proposal["proposal"].team, 
                purchase=purchase,  
                proposal=proposal["proposal"], 
                sales_price=int(proposal["salary"]), 
                staff_hired=proposal["member_qty"],
                earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),                   
                total_earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value),
                total_discount_offered=((get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"])                     
            )

        for proposal in hiringbox:
            SalesReporting.objects.create(
                client=request.user,
                team=proposal["proposal"].team, 
                purchase=purchase,  
                sales_category=SalesReporting.PROPOSAL, 
                sales_price=int(proposal["salary"]),  
                staff_hired=proposal["member_qty"],
                client_fee_charged=round(shared_gateway_fee),
                freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                total_freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=round(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_discount_offered=(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"]) 
            )
        auth_token = flutterwaveClient.flutterwave_secret_key()
        headers = {'Authorization': 'Bearer ' + auth_token}
        data = {
            "tx_ref": unique_reference,
            "amount": grand_total,
            "currency": base_currency,
            "redirect_url": "http://127.0.0.1:8000/transaction/flutter_success/",
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

        url = 'https://api.flutterwave.com/v3/payments'
        response = requests.post(url, json=data, headers=headers)
        response_to_json = response.json()
        redirectToCheckout = response_to_json['data']['link']

        return JsonResponse({'redirectToCheckout': redirectToCheckout})


def get_flutterwave_verification(unique_reference, flutterwave_order_key):
    Purchase.objects.filter(
        unique_reference=unique_reference, 
        status=Purchase.FAILED,        
    ).update(status=Purchase.SUCCESS, flutterwave_order_key=flutterwave_order_key)


@require_http_methods(['POST'])
@csrf_exempt
def flutterwave_webhook(request):
    flutterwaveClient = FlutterwaveClientConfig()
    secret_hash = flutterwaveClient.flutterwave_secret_hash()
    signature = request.headers.get("verifi-hash")
    print('signature:', signature)

    payload = request.body
    print('payload:',payload)

    if signature == None or (signature != secret_hash):
        # This request isn't from Flutterwave; discard
        return HttpResponse(status=401)

    payload = request.body
    print(payload)
    # status = payload['success']
    # Do something (that doesn't take too long) with the payload
    return HttpResponse(status=200)

    
@login_required
@user_is_client
@require_http_methods(['GET', 'POST'])
def flutter_success(request):
    hiringbox = HiringBox(request)
    status = request.GET.get('status', None)
    unique_reference = request.GET.get('tx_ref', '')
    flutterwave_order_key = request.GET.get('transaction_id', '')
    message = ''
    if status == 'successful' and unique_reference != '' and flutterwave_order_key != '':
        get_flutterwave_verification(unique_reference, flutterwave_order_key)
        
        message = 'Payment succeeded'
    else:
        message = 'Payment failed'
        return HttpResponse(status=401)
       
    # hiringbox.clean_box()
    context = {
        "message": message
    }
    return render(request, "applications/payment_success.html", context)


@login_required
def stripe_payment_order(request):
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    gateway_type = hiringbox.get_gateway()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    number_of_applicants = hiringbox.__len__()
    shared_gateway_fee = total_gateway_fee/number_of_applicants
    grand_total = hiringbox.get_total_price_after_discount_and_fee()

    stripe_obj = StripeClientConfig()
    stripe_reference = stripe_obj.stripe_unique_reference()
    stripe.api_key = stripe_obj.stripe_secret_key()

    session = stripe.checkout.Session.create(
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
        success_url='http://' + str(get_current_site(request)) + '/transaction/congrats/',
        cancel_url='http://' + str(get_current_site(request)) + '/dashboard/'
    )
    gateway_type = str(hiringbox.get_gateway())
    payment_intent = session.payment_intent

    if Purchase.objects.filter(stripe_order_key=payment_intent).exists():
        pass
    else:
        purchase = Purchase.objects.create(
            client=request.user,
            full_name=request.user.get_full_name,
            email=request.user.email,
            country=str(request.user.country),
            payment_method=gateway_type,
            salary_paid=grand_total,
            unique_reference=stripe_reference,           
        )           
        purchase.stripe_order_key=payment_intent
        purchase.status=Purchase.FAILED
        purchase.save()

        for proposal in hiringbox:
            ProposalSale.objects.create(
                team=proposal["proposal"].team, 
                purchase=purchase,  
                proposal=proposal["proposal"], 
                sales_price=int(proposal["salary"]), 
                staff_hired=proposal["member_qty"],
                earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),                   
                total_earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value),
                total_discount_offered=((get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"]) 
            )

        for proposal in hiringbox:
            SalesReporting.objects.create(
                client=request.user,
                team=proposal["proposal"].team, 
                purchase=purchase,  
                sales_category=SalesReporting.PROPOSAL, 
                sales_price=int(proposal["salary"]), 
                staff_hired=proposal["member_qty"],
                client_fee_charged=round(shared_gateway_fee),
                freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                total_freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=round(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_discount_offered=(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"]) 
            )
        hiringbox.clean_box()
        return JsonResponse({'session': session,})
            
    hiringbox.clean_box()
    return JsonResponse({'failed':'Bad Signature',})
    

def stripe_specific_payment_confirmation(data):
    Purchase.objects.filter(stripe_order_key=data).update(status=Purchase.SUCCESS)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    stripe.api_key = StripeClientConfig().stripe_secret_key()
    webhook_key = StripeClientConfig().stripe_webhook_key()    
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    team = ''
    package = ''
    

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_key)
    except ValueError as e:
        # returns Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # returns Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == 'paid':
            try:
                stripe_specific_payment_confirmation(session.payment_intent)            
                team = Team.objects.get(pk=session.get('client_reference_id'))
                team.stripe_customer_id = session.get('customer')
                team.stripe_subscription_id = session.get('subscription')
                team.save()
                
                package = Package.objects.get(is_default=False, type='Team')
                SubscriptionItem.objects.create(
                    team=team,
                    customer_id = team.stripe_customer_id,
                    subscription_id=team.stripe_subscription_id,
                    payment_method='Stripe', 
                    price=package.price, 
                    created_at = timezone.now(),
                    activation_time = timezone.now(),
                    expired_time = get_expiration(),
                    status = True,
                )
                           
            except:
                print('Payment unsuccessful')
        else:
            print('Payment unsuccessful')  

    return HttpResponse(status=200)
  

@login_required
def paypal_payment_order(request):
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    gateway_type = hiringbox.get_gateway()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()

    number_of_applicants = hiringbox.__len__()
    shared_gateway_fee = total_gateway_fee/number_of_applicants

    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)
    data = body["orderID"]
    print(data)

    if data:
        paypal_request_order = OrdersGetRequest(data)
        response = PayPalClient.paypal_httpclient().execute(paypal_request_order)

        purchase = Purchase.objects.create(
            client=request.user,
            full_name=response.result.purchase_units[0].shipping.name.full_name,
            email=response.result.payer.email_address,
            country = request.user.country,
            payment_method=str(gateway_type),
            salary_paid=round(float(response.result.purchase_units[0].amount.value)),
            paypal_order_key=response.result.id,
            unique_reference=PayPalClient.paypal_unique_reference(),
            status = Purchase.SUCCESS
        )

        for proposal in hiringbox:
            ProposalSale.objects.create(
                team=proposal["proposal"].team, 
                purchase=purchase,  
                proposal=proposal["proposal"], 
                sales_price=int(proposal["salary"]), 
                staff_hired=proposal["member_qty"],
                earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),                   
                total_earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value),
                total_discount_offered=((get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"]) 

            )

        for proposal in hiringbox:
            SalesReporting.objects.create(
                client=request.user,
                team=proposal["proposal"].team, 
                purchase=purchase,  
                sales_category=SalesReporting.PROPOSAL, 
                sales_price=int(proposal["salary"]), 
                staff_hired=proposal["member_qty"],
                client_fee_charged=round(shared_gateway_fee),
                freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                total_freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=round(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_discount_offered=(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"])             
            )
    else:
        purchase.status = Purchase.FAILED
        purchase.save()
        return JsonResponse({'failed':'Bad Signature, Razorpay will refund your money if you are already debited',})
            
    hiringbox.clean_box()
    return JsonResponse({'Perfect':'All was successful',})


@login_required
@user_is_client
def razorpay_application_intent(request):
    hiringbox = HiringBox(request)
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    gateway_type = hiringbox.get_gateway()
    base_currency_code = get_base_currency_code()
    
    razorpay_api = RazorpayClientConfig()
    unique_reference = razorpay_api.razorpay_unique_reference()

    purchase = Purchase.objects.create(
        client=request.user,
        full_name=f'{request.user.first_name} {request.user.last_name}',
        payment_method=str(gateway_type),
        salary_paid=grand_total,
        unique_reference=unique_reference,
        status = Purchase.FAILED
    )

    notes = {'Total Price': 'The total amount may change with discount'}
    currency = base_currency_code
    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_order = razorpay_client.order.create(dict(
        amount = grand_total * 100, 
        currency = currency, 
        notes = notes, 
        receipt = purchase.unique_reference
    ))
    print('razorpay_order', razorpay_order['id'])
    purchase.razorpay_order_key = razorpay_order['id']
    purchase.save()

    response = JsonResponse({'currency':currency, 'amount': (purchase.salary_paid), 'razorpay_order_key': purchase.razorpay_order_key})
    return response


@login_required
@user_is_client
def razorpay_webhook(request):
    hiringbox = HiringBox(request)      
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    total_after_discount_only = hiringbox.get_total_price_after_discount_only()
    print('total_after_discount_only :', total_after_discount_only)
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total_after_expense = hiringbox.get_total_price_after_discount_and_fee()
    number_of_applicants = hiringbox.__len__()
    shared_gateway_fee = total_gateway_fee/number_of_applicants
    
    razorpay_client = RazorpayClientConfig().get_razorpay_client()
    if request.POST.get('action') == 'razorpay-proposal':   
        razorpay_order_key = request.POST.get('orderid')
        razorpay_payment_id = request.POST.get('paymentid')
        razorpay_signature = request.POST.get('signature')
        
        data ={
            'razorpay_order_id': razorpay_order_key,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        purchase = Purchase.objects.get(razorpay_order_key=razorpay_order_key)
        purchase.razorpay_payment_id = razorpay_payment_id
        purchase.razorpay_signature = razorpay_signature
        purchase.save()

        signature = razorpay_client.utility.verify_payment_signature(data)

        if signature == True:
            purchase.status = Purchase.SUCCESS
            purchase.save()
            
            for proposal in hiringbox:
                ProposalSale.objects.create(
                    team=proposal["proposal"].team, 
                    purchase=purchase,  
                    proposal=proposal["proposal"], 
                    sales_price=int(proposal["salary"]),
                    staff_hired=proposal["member_qty"],
                    earning_fee_charged=int(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),                   
                    total_earning_fee_charged=int(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                    discount_offered=get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value),
                    total_discount_offered=((get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                    disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                    total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                    earning=int(get_earning_calculator(
                        (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                        get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                    total_earning=int(get_earning_calculator(
                        (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                        get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"]) 
                )

            for proposal in hiringbox:
                SalesReporting.objects.create(
                    client=request.user,
                    team=proposal["proposal"].team, 
                    purchase=purchase,  
                    sales_category=SalesReporting.PROPOSAL, 
                    sales_price=int(proposal["salary"]),
                    staff_hired=proposal["member_qty"],
                    freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    total_freelancer_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                    discount_offered=round(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                    total_discount_offered=(get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value) * proposal["member_qty"]),
                    disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                    total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                    earning=int(get_earning_calculator(
                        (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                        get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                    total_earning=int(get_earning_calculator(
                        (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                        get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"])
                )
        else:
            purchase.status = Purchase.FAILED
            purchase.save()
            return JsonResponse({'failed':'Bad Signature, Razorpay will refund your money if you are already debited',})
            
    hiringbox.clean_box()
    return JsonResponse({'Perfect':'All was successful',})
                

@login_required
def payment_success(request):
    # hiringbox = HiringBox(request)
    # hiringbox.clean_box()

    context = {
        "good": "good"
    }
    return render(request, "transactions/payment_success.html", context)


@login_required
def proposal_transaction(request):
    base_currency = get_base_currency_code()
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)    
        proposals = ProposalSale.objects.filter(team=team, purchase__status=Purchase.SUCCESS)

    elif request.user.user_type == Customer.CLIENT:
        proposals = ProposalSale.objects.filter(purchase__client=request.user, purchase__status=Purchase.SUCCESS)

    context = {
        'proposals': proposals,
        'base_currency': base_currency,

    }
    return render(request, 'transactions/proposal_transactions.html', context)


@login_required
def application_transaction(request):
    base_currency = get_base_currency_code()
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)   
        applications = ApplicationSale.objects.filter(team=team, purchase__status=Purchase.SUCCESS)

    elif request.user.user_type == Customer.CLIENT:
        applications = ApplicationSale.objects.filter(purchase__client=request.user, purchase__status=Purchase.SUCCESS)
    
    context = {
        'applications':applications,
        'base_currency': base_currency,        
    }
    return render(request, 'transactions/application_transactions.html', context)


@login_required
def contract_transaction(request):
    base_currency = get_base_currency_code()
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)   
        contracts = ContractSale.objects.filter(team=team, contract__status=InternalContract.PAID, purchase__status=Purchase.SUCCESS)

    elif request.user.user_type == Customer.CLIENT:
        contracts = ContractSale.objects.filter(contract__status=InternalContract.PAID, purchase__client=request.user, purchase__status=Purchase.SUCCESS)

    context = {
        'contracts':contracts,
        'base_currency': base_currency,        
    }
    return render(request, 'transactions/contract_transactions.html', context)

