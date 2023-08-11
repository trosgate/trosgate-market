import stripe
import json
import requests
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
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
from payments.paypal import PayPalClientConfig
from payments.stripe import StripeClientConfig
from payments.razorpay import RazorpayClientConfig
from payments.flutterwave import FlutterwaveClientConfig
from payments.paystack import PaystackClientConfig
from .utilities import get_base_currency, calculate_payment_data, PurchaseAndSaleCreator

from django.views.decorators.csrf import csrf_exempt
from .models import (
    ApplicationSale, 
    Purchase, 
    ProposalSale, 
    ContractSale, 
    SubscriptionItem
)
from .hiringbox import HiringBox
from general_settings.fees_and_charges import get_proposal_fee_calculator
# from general_settings.currency import get_base_currency_symbol, get_base_currency_code
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
from django_htmx.http import HttpResponseClientRedirect
from payments.forms import StripeCardCardForm
from account.models import Merchant



@login_required
def add_proposal_to_box(request):
    # Callable function for adding proposal and
    # modifying the quantity of freelancer in the box
    hiringbox = HiringBox(request)

    if request.POST.get('action') == 'post':
        proposal_id = int(request.POST.get('proposalid'))
        member_qty = int(request.POST.get('memberqty'))
        package_price = int(request.POST.get('salary'))
        package = str(request.POST.get('package'))

        proposal = get_object_or_404(Proposal, id=proposal_id, status=Proposal.ACTIVE)

        if proposal.pricing == True:
            hiringbox.set_pricing(proposal=proposal.id, package_name=package, package_price=package_price)
            hiringbox.addon(proposal=proposal, member_qty=member_qty, salary=package_price, package_name=package)
        else:
            hiringbox.addon(proposal=proposal, member_qty=member_qty, salary=proposal.salary, package_name='single')
        
        memberqty = hiringbox.__len__()
        total = package_price * member_qty
        base_currency = get_base_currency(request)
        readable_amount = f'{base_currency} {total}'
        
        response = JsonResponse(
            {'salary': readable_amount, 'member_qty': memberqty})
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
        payment_data = calculate_payment_data(hiringbox)
        freelancers = hiringbox.__len__()
        base_currency = get_base_currency(request)
        response = JsonResponse({
            'freelancers': freelancers,
            'base_currency':base_currency,
            'subtotal': payment_data['grand_total_before_expense'],
            'grand_total': payment_data['grand_total'],
            'selected_fee': payment_data['total_gateway_fee'],
            "discount": payment_data['discount_value'],
        })
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
        proposal = get_object_or_404(Proposal, id=proposal_id, status=Proposal.ACTIVE)
        
        member_qty = int(request.POST.get('memberqty'))
        hiringbox.modify(proposal=proposal.id, member_qty=member_qty, price=proposal.salary)

        line_total_price = member_qty * proposal.salary
        freelancers = hiringbox.__len__()
        grand_total = hiringbox.get_total_price_before_fee_and_discount()
        base_currency = get_base_currency(request)
        discount = hiringbox.get_discount_value()
        response = JsonResponse({
            'freelancers': freelancers, 
            'grandtotal': grand_total, 
            'total_price': line_total_price,
            'base_currency':base_currency,
            'discount':discount
        })
        return response


@login_required
def pricing_option_with_fees(request):
    hiringbox = HiringBox(request)
    base_currency = get_base_currency(request)
    payment_gateways = request.merchant.merchant.gateways.all().exclude(name='balance')

    if request.method == 'POST':
        gateways = int(request.POST.get('paymentGateway'))
        gateway = PaymentGateway.objects.filter(id=gateways).first()
        session = request.session

        if gateway: 
            if "proposalgateway" not in request.session:
                session["proposalgateway"] = {"gateway_id": gateway.id}
                session.modified = True
            else:
                session["proposalgateway"]["gateway_id"] = gateway.id
                session.modified = True
        else:
            pass
    payment_data = calculate_payment_data(hiringbox)
    context ={
        'selected': 'selected',
        'hiringbox': hiringbox,
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
        return render(request, "transactions/partials/pricing_option_with_fees.html", context)

    return render(request, "transactions/pricing_option_with_fees.html", context)


@login_required
def payment_fee_structure(request):
    hiringbox = HiringBox(request)
    gateway_type = int(request.POST.get('paymentGateway'))
    gateway = PaymentGateway.objects.get(id=gateway_type)
    selected_fee = gateway.processing_fee
    payment_gateways = request.merchant.merchant.gateways.all().exclude(name='balance')
    base_currency = get_base_currency(request)
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
        'hiringbox': hiringbox,
        'payment_gateways': payment_gateways,
        'base_currency': base_currency,
        'payment_method': 'Payment Summary',
        'subtotal': subtotal,
        'selected_fee': selected_fee,
        "gateway_type": gateway_type,        
    }


    return render(request, "transactions/partials/pricing_option_with_fees.html", context)


@login_required
def final_checkout(request):
    hiringbox = HiringBox(request)
    payment_data = calculate_payment_data(hiringbox)
    num_of_freelancers = hiringbox.__len__()

    if num_of_freelancers < 1:
        messages.error(request, "Please add atleast one proposal to proceed")
        return redirect("transactions:pricing_option_with_fees")

    if  "proposalgateway" not in request.session:
        messages.error(request, "Please select payment option")
        return redirect("transactions:pricing_option_with_fees")

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

    return render(request, "transactions/final_proposal_checkout.html", context)


@login_required
@user_is_client
def paystack_payment_intent(request):
    hiringbox = HiringBox(request)
    payment_data = calculate_payment_data(hiringbox)
    purchase = None

    try:
        creator = PurchaseAndSaleCreator()
        purchase = creator.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.PROPOSAL,
            hiringbox=hiringbox,
        )
        response_data = {
            'reference': purchase.reference,
            'amount': (purchase.salary_paid * 100),
            'email': request.user.email,
            'currency': str(purchase.merchant.merchant.country.currency).upper(),
        }
        
        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'error': 'Error Occured'})


@csrf_exempt
def paystack_callback(request):
    hiringbox = HiringBox(request)      
    payment_reference = request.POST.get('payment_reference')
    transaction_id = request.POST.get('transaction_reference')
    message = request.POST.get('message')
    status = request.POST.get('status')

    try:
        
        if status == 'success' and message == 'Approved':
            Purchase.paystack_order_confirmation(
                payment_reference, transaction_id
            )
            hiringbox.clean_box()
            return JsonResponse({
                'status': 'success', 
                'transaction_url': '/transaction/proposals/'}
            )
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
  

@login_required
@user_is_client
def flutter_payment_intent(request):
    hiringbox = HiringBox(request)
    payment_data = calculate_payment_data(hiringbox)
    purchase = None

    try:
        creator = PurchaseAndSaleCreator()
        purchase = creator.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.PROPOSAL,
            hiringbox=hiringbox,
        )
        currency = str(purchase.merchant.merchant.country.currency).upper()
        base_currency = get_base_currency(request)
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
    hiringbox = HiringBox(request)
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

            hiringbox.clean_box()
            data = {"status": "success", 'redirect_url':'/transaction/flutter_success/'}
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
    hiringbox = HiringBox(request)
    payment_data = calculate_payment_data(hiringbox)
    grand_total = hiringbox.get_total_price_after_discount_and_fee()

    card_token = request.POST.get('card_token')
    stripe_client = StripeClientConfig()
    payment_id, client_secret = stripe_client.create_payment_intent(grand_total,card_token) 
    purchase = None
    try:
        creator = PurchaseAndSaleCreator()
        purchase = creator.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.PROPOSAL,
            stripe_order_key=payment_id,
            hiringbox=hiringbox,
        )
        response_data = {
            'client_secret': client_secret,
            'payment_intent': payment_id,
        }
        print('purchase ID ::', purchase.id)
        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'status': 'failed'})


@login_required
@require_http_methods(['POST'])
def stripe_payment_order(request):
    hiringbox = HiringBox(request)

    stripe_order_key = request.POST.get('stripe_order_key')
    Purchase.stripe_order_confirmation(stripe_order_key)
    hiringbox.clean_box()
    transaction_url = reverse('transactions:proposal_transaction') 
    return JsonResponse({'status': 'success', 'transaction_url':transaction_url})
    

@login_required
def paypal_payment_order(request):
    hiringbox = HiringBox(request)
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    payment_data = calculate_payment_data(hiringbox)
    purchase = None

    paypal_order_key = PayPalClientConfig().create_order(grand_total)
    if paypal_order_key:
        try:
            creator = PurchaseAndSaleCreator()
            purchase = creator.create_purchase_and_sales(
                client=request.user,
                **payment_data,
                category=Purchase.PROPOSAL,
                paypal_order_key=paypal_order_key,
                hiringbox=hiringbox,
            )
            response_data = {
                'paypal_order_key': paypal_order_key,
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
@csrf_exempt
@require_http_methods(['POST'])
def paypal_callback(request):
    hiringbox = HiringBox(request)

    body = json.loads(request.body)
    paypal_order_key = body["paypal_order_key"]

    capture_data = PayPalClientConfig().capture_order(paypal_order_key,)
    capture_data_id = capture_data['purchase_units'][0]['payments']['captures'][0]['id']
    if capture_data['status'] == 'COMPLETED':
        Purchase.paypal_order_confirmation(paypal_order_key, capture_data_id)
        hiringbox.clean_box()
        return JsonResponse(capture_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@login_required
@user_is_client
def razorpay_application_intent(request):

    hiringbox = HiringBox(request)
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    payment_data = calculate_payment_data(hiringbox)
    purchase = None
    merchant = Merchant.objects.filter(pk=request.user.active_merchant_id).first()
    base_currency = get_base_currency(request)
    razorpay_order_key = RazorpayClientConfig().create_order(grand_total)
    if razorpay_order_key:
        try:
            creator = PurchaseAndSaleCreator()
            purchase = creator.create_purchase_and_sales(
                client=request.user,
                **payment_data,
                category=Purchase.PROPOSAL,
                razorpay_order_key=razorpay_order_key,
                hiringbox=hiringbox,
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
    hiringbox = HiringBox(request)      
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
            hiringbox.clean_box()
            return JsonResponse({'status':'success','transaction_url':'/transaction/proposals/'})
        except Exception as e:
            print('%s' % (str(e)))
            return JsonResponse({'status':'error'}) 

    else:
        return JsonResponse({'status':'error'})
 
                
@login_required
def payment_success(request):

    context = {
        "good": "good"
    }
    return render(request, "transactions/payment_success.html", context)


@login_required
def proposal_transaction(request):
    base_currency = get_base_currency(request)
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
    base_currency = get_base_currency(request)
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
    base_currency = get_base_currency(request)
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

