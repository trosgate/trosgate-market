import stripe
import json
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
from teams.models import Team
from account.models import Package
from proposals.models import Proposal
from paypalcheckoutsdk.orders import OrdersGetRequest
from payments.models import PaymentGateway
from general_settings.gateways import PayPalClientConfig, StripeClientConfig, FlutterwaveClientConfig, RazorpayClientConfig
from django.views.decorators.csrf import csrf_exempt
from .models import ApplicationSale, Purchase, ProposalSale, ContractSale, SubscriptionItem
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
from teams.utilities import get_expiration
from django.db import transaction as db_transaction
from freelancer.models import FreelancerAccount
from general_settings.utilities import get_protocol_only
from client.models import ClientAccount


@login_required
def proposal_direct_hire(request, short_name, proposal_slug):
    '''
    A page for hiring single freelancer directly
    In frontend, the proposal is captured into session when client proceeds 
    '''
    proposal = get_object_or_404(Proposal, created_by__short_name=short_name,  slug=proposal_slug)

    context = {
        'proposal': proposal,
    }
    return render(request, "transactions/proposal_single_summary.html", context)


@login_required
def proposal_bucket(request):
    # This function provides a collection of all proposals in bucket
    hiringbox = HiringBox(request)
    context={
        'hiringbox': hiringbox
    }
    return render(request, "transactions/proposal_bucket.html", context)


@login_required
def add_proposal_to_box(request):
    '''
    Callable function for adding proposal and
    modifying the quantity of freelancer in the box
    '''
    hiringbox = HiringBox(request)

    if request.POST.get('action') == 'post':
        proposal_id = int(request.POST.get('proposalid'))
        member_qty = int(request.POST.get('memberqty'))
        proposal = get_object_or_404(Proposal, id=proposal_id, status=Proposal.ACTIVE)

        hiringbox.addon(proposal=proposal, member_qty=member_qty)
        memberqty = hiringbox.__len__()
        totals = hiringbox.get_total_price_before_fee_and_discount()

        response = JsonResponse(
            {'salary': proposal.salary, 'member_qty': memberqty, 'get_totals': totals})
        return response


@login_required
def remove_from_hiring_box(request):
    '''
    Callable function for removing proposal and
    associated quantity of freelancer from box
    '''
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
    '''
    Callable CRUD function for modifying proposal and
    associated quantity of freelancer within hiring box
    '''
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
    # function for selecting checkout option
    hiringbox = HiringBox(request)

    if hiringbox.__len__() < 1:
        messages.error(request, "Please add atleast one proposal to proceed")
        return redirect("transactions:hiring_box_summary")

    payment_gateways = request.merchant.merchant.gateways.all().exclude(name='balance')
    base_currency = get_base_currency_symbol()    
    context ={
        'hiringbox': hiringbox,
        'payment_gateways': payment_gateways,
        'base_currency': base_currency
    }
    return render(request, "transactions/payment_option_with_fees.html", context)


@login_required
def payment_fee_structure(request):
    '''
    Callable function for updating the fees
    Adding fee ID as an object to session
    Adding to session makes it easy to retrieve selected fee on checkout page
    '''
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
    # Final checkout page
    # Step 1: Checks if atleast one proposal was selected previously
    # Step 2: Checks if gateway option was selected previously
    # If step 1 & 2 are true, user can procced wit checkout
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
    # Callable function for interacting with flutterwave api
    # Flutterwave particularly require unique id for each client. 
    # The system generates new code, checks in advance for unique ID from database before saving new one
    # Per client request, the transaction is initially saved into the database with the status of unpaid
    # A different callback webhook listens for the success and ,. 
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    gateway_type = str(hiringbox.get_gateway())
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    base_currency = get_base_currency_code()

    flutterwaveClient = FlutterwaveClientConfig()
    unique_reference = flutterwaveClient.flutterwave_unique_reference()

    if Purchase.objects.filter(unique_reference=unique_reference).exists():
        pass
    else:       
        try:
            purchase = Purchase.objects.create(
                payment_method=gateway_type,
                client_fee = int(total_gateway_fee),
                category = Purchase.PROPOSAL,
                salary_paid=grand_total,
                unique_reference=unique_reference,           
            )           

            purchase.status=Purchase.FAILED
            purchase.save()
        except Exception as e:
            print('%s' % (str(e)))

        try:
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
        except Exception as e:
            print('%s' % (str(e)))

        redirect_url= f"{get_protocol_only()}{str(get_current_site(request))}/transaction/flutter_success/",
        auth_token = flutterwaveClient.flutterwave_secret_key()
        headers = {'Authorization': 'Bearer ' + auth_token}
        data = {
            "tx_ref": unique_reference,
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

        url = 'https://api.flutterwave.com/v3/payments'
        response = requests.post(url, json=data, headers=headers)
        response_to_json = response.json()
        redirectToCheckout = response_to_json['data']['link']

        return JsonResponse({'redirectToCheckout': redirectToCheckout})


# @require_http_methods(['POST'])
# @csrf_exempt
# def flutterwave_webhook(request):
#     flutterwaveClient = FlutterwaveClientConfig()
#     secret_hash = flutterwaveClient.flutterwave_secret_hash()
#     signature = request.headers.get("verifi-hash")
#     print('signature:', signature)

#     payload = request.body
#     print('payload:',payload)

#     if signature == None or (signature != secret_hash):
#         # This request isn't from Flutterwave; discard
#         return HttpResponse(status=401)

#     payload = request.body
#     print(payload)
#     # status = payload['success']
#     # Do something (that doesn't take too long) with the payload
#     return HttpResponse(status=200)

    
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
        Purchase.flutterwave_order_confirmation(unique_reference=unique_reference, flutterwave_order_key=flutterwave_order_key)
        message = 'Payment succeeded'
    else:
        message = 'Payment failed'
        return HttpResponse(status=401)
       
    hiringbox.clean_box()
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
    grand_total = hiringbox.get_total_price_after_discount_and_fee()


    stripe_checkout = StripeClientConfig()
    success_url=f"{get_protocol_only()}{str(get_current_site(request))}/transaction/congrats/",
    cancel_url=f"{get_protocol_only()}{str(get_current_site(request))}/dashboard/",

    session = stripe_checkout.create_checkout(
        amount=grand_total, 
        currency='usd', 
        customer_email=request.user.email, 
        success_url=success_url,
        cancel_url=cancel_url
    )

    payment_intent = session.payment_intent
    gateway_type = str(hiringbox.get_gateway())

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
                category = Purchase.PROPOSAL,
                payment_method=gateway_type,
                salary_paid=grand_total           
            )
            purchase.stripe_order_key=payment_intent
            purchase.status=Purchase.FAILED
            purchase.save()
        except Exception as e:
            print('%s' % (str(e)))

        try:
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
        except Exception as e:
            print('%s' % (str(e)))

        hiringbox.clean_box()
        return JsonResponse({'session': session,})
            
    return JsonResponse({'failed':'Bad Signature',})


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
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == 'paid':

            if session.mode == 'payment' and session['metadata']['mode'] == 'payment':
                try:
                    Purchase.stripe_order_confirmation(session.payment_intent)                    
                except Exception as e:
                    print('%s' % (str(e)))

            if session.mode == 'payment' and session['metadata']['mode'] == 'deposit':
                try:
                    deposit_fee = session['metadata']['deposit_fee']
                    deposit_gateway = session['metadata']['gateway']
                    narration = session['metadata']['narration']
                    amount_total = session.get('amount_total')
                    convert_fee = int(deposit_fee)
                    convert_amount = int(amount_total)
                    value_returned = int((convert_amount/100) - convert_fee)

                    ClientAccount.final_deposit(
                        user=session.get('client_reference_id'), 
                        amount=value_returned, 
                        deposit_fee=convert_fee, 
                        narration=narration, 
                        gateway=deposit_gateway
                    )                    
                except Exception as e:
                    print('%s' % (str(e)))

            if session.mode == 'subscription':
                try:                            
                    package = Package.objects.get(is_default=False, type='Team')
                    team = Team.objects.get(pk=session.get('client_reference_id'))
                    team.stripe_customer_id = session.get('customer')
                    team.stripe_subscription_id = session.get('subscription')
                    team.package = package
                    team.package_status = Team.ACTIVE
                    team.package_expiry = get_expiration()
                    team.save()   

                except Exception as e:
                    print('%s' % (str(e)))

                try:
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
                            
                except Exception as e:
                    print('%s' % (str(e)))
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
    purchase = ''

    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)
    data = body["orderID"]

    purchase = ''
    paypal_request_order = OrdersGetRequest(data)
    response = PayPalClient.paypal_httpclient().execute(paypal_request_order)

    if response:
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                full_name=response.result.purchase_units[0].shipping.name.full_name,
                email=response.result.payer.email_address,
                country = request.user.country,
                payment_method=str(gateway_type),
                client_fee = int(total_gateway_fee),
                category = Purchase.PROPOSAL,
                salary_paid=round(float(response.result.purchase_units[0].amount.value)),
                paypal_order_key=response.result.id,
                unique_reference=PayPalClient.paypal_unique_reference(),
                status = Purchase.FAILED
            )
        except Exception as e:
            print('%s' % (str(e)))
        
        try:    
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

        except Exception as e:
            print('%s' % (str(e)))

        try:
            Purchase.paypal_order_confirmation(pk=purchase.pk)
        except Exception as e:
            print('%s' % (str(e)))        

        hiringbox.clean_box()
        return JsonResponse({'Perfect':'All was successful',})
    else:
        purchase.status = Purchase.FAILED
        purchase.save()
        return JsonResponse({'failed':'Bad Signature, Razorpay will refund your money if you are already debited',})
            

@login_required
@user_is_client
def razorpay_application_intent(request):
    hiringbox = HiringBox(request)
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    gateway_type = hiringbox.get_gateway()
    base_currency_code = get_base_currency_code()
    total_gateway_fee = hiringbox.get_fee_payable()
    discount_value = hiringbox.get_discount_value()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()

    razorpay_api = RazorpayClientConfig()
    unique_reference = razorpay_api.razorpay_unique_reference()
    try:
        purchase = Purchase.objects.create(
            client=request.user,
            full_name=f'{request.user.first_name} {request.user.last_name}',
            payment_method=str(gateway_type),
            client_fee = int(total_gateway_fee),
            category = Purchase.PROPOSAL,
            salary_paid=grand_total,
            unique_reference=unique_reference,
            status = Purchase.FAILED
        )
    except Exception as e:
        print('%s' % (str(e)))

    try:
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
    except Exception as e:
        print('%s' % (str(e)))

    notes = {'Total Price': 'The total amount may change with discount'}
    currency = base_currency_code
    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_order = razorpay_client.order.create(dict(
        amount = grand_total * 100, 
        currency = currency, 
        notes = notes, 
        receipt = purchase.unique_reference
    ))

    purchase.razorpay_order_key = razorpay_order['id']
    purchase.save()

    response = JsonResponse({'currency':currency, 'amount': (purchase.salary_paid), 'razorpay_order_key': purchase.razorpay_order_key})
    return response


@login_required
@user_is_client
def razorpay_webhook(request):
    hiringbox = HiringBox(request)      
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

        signature = razorpay_client.utility.verify_payment_signature(data)

        if signature == True:
            try:
                Purchase.razorpay_order_confirmation(razorpay_order_key, razorpay_payment_id, razorpay_signature)
                hiringbox.clean_box()
                return JsonResponse({'Perfect':'All was successful',})
            except Exception as e:
                print('%s' % (str(e))) 

        else:
            return JsonResponse({'failed':'Transaction failed, Razorpay will refund your money if you are already debited',})
 
                
@login_required
def payment_success(request):

    context = {
        "good": "good"
    }
    return render(request, "transactions/payment_success.html", context)


@login_required
def proposal_transaction(request):
    base_currency = get_base_currency_code()
    proposals = None
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
    applications = None
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
    contracts = None
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)   
        contracts = ContractSale.objects.filter(team=team, purchase__status=Purchase.SUCCESS)

    elif request.user.user_type == Customer.CLIENT:
        contracts = ContractSale.objects.filter(purchase__client=request.user, purchase__status=Purchase.SUCCESS)
    
    context = {
        'contracts':contracts,
        'base_currency': base_currency,        
    }
    return render(request, 'transactions/contract_transactions.html', context)


# @login_required
# def one_click_transaction(request):
#     base_currency = get_base_currency_code()
#     oneclicks = ''
#     if request.user.user_type == Customer.FREELANCER:
#         team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)   
#         oneclicks = OneClickPurchase.objects.filter(team=team, status=OneClickPurchase.SUCCESS)

#     elif request.user.user_type == Customer.CLIENT:
#         oneclicks = OneClickPurchase.objects.filter(client=request.user, status=OneClickPurchase.SUCCESS)

#     context = {
#         'oneclicks':oneclicks,
#         'base_currency': base_currency,        
#     }
#     return render(request, 'transactions/oneclicks_transactions.html', context)


