import stripe
import json
import requests
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
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
from django_htmx.http import HttpResponseClientRedirect
from payments.forms import StripeCardCardForm


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
        base_currency = get_base_currency_symbol()
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
        freelancers = hiringbox.__len__()
        grand_total = hiringbox.get_total_price_before_fee_and_discount()
        base_currency = get_base_currency_symbol()
        discount = hiringbox.get_discount_value()
        response = JsonResponse({
            'freelancers': freelancers, 
            'grandtotal': grand_total,
            'base_currency':base_currency,
            'discount':discount
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
        base_currency = get_base_currency_symbol()
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
    # function for selecting checkout payment option
    payment_gateways = request.merchant.merchant.gateways.all().exclude(name='balance')

    hiringbox = HiringBox(request)
    base_currency = get_base_currency_symbol()
    base_currency_code = get_base_currency_code()
    gateway_type = hiringbox.get_gateway()
    selected_fee = hiringbox.get_fee_payable()
    discount = hiringbox.get_discount_value()
    subtotal = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    
    if request.method == 'POST':
        gateways = int(request.POST.get('paymentGateway'))
        gateway = PaymentGateway.objects.get(id=gateways)
        selected_fee = gateway.processing_fee
        gateway_type = gateway.name
        session = request.session

        if "proposalgateway" not in request.session:
            session["proposalgateway"] = {"gateway_id": gateway.id}
            session.modified = True
        else:
            session["proposalgateway"]["gateway_id"] = gateway.id
            session.modified = True

    context ={
        'selected': 'selected',
        'hiringbox': hiringbox,
        'payment_gateways': payment_gateways,
        'base_currency': base_currency,
        'base_currency_code': base_currency_code,
        'payment_method': 'Payment Summary',
        'subtotal': subtotal,
        'grand_total': grand_total,
        'selected_fee': selected_fee,
        "gateway_type": gateway_type,
        "discount": discount,
    
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
    base_currency = get_base_currency_symbol()
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
    num_of_freelancers = hiringbox.__len__()

    if num_of_freelancers < 1:
        messages.error(request, "Please add atleast one proposal to proceed")
        return redirect("transactions:pricing_option_with_fees")

    if  "proposalgateway" not in request.session:
        messages.error(request, "Please select payment option")
        return redirect("transactions:pricing_option_with_fees")

    gateway_type = hiringbox.get_gateway().name

    selected_fee = hiringbox.get_fee_payable()
    subtotal = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    subtotal = hiringbox.get_total_price_before_fee_and_discount()
    base_currency = get_base_currency_code()

    paypal_public_key = ''
    stripeClient = ''
    razorpay_public_key = ''
    flutterwave_public_key = ''
    stripe_public_key = ''

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

    # print(request.build_absolute_uri(reverse('transactions:proposal_transaction')))
    context = {
        'subtotal': subtotal,
        'grand_total': grand_total,
        'selected_fee': selected_fee,
        "gateway_type": gateway_type,
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
def flutter_payment_intent(request):
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    gateway_type = str(hiringbox.get_gateway())
    base_currency = str(get_base_currency_code()).lower()

    redirect_url = f"{get_protocol_only()}{str(get_current_site(request))}/transaction/proposals/",
    flutterwave, tx_ref = FlutterwaveClientConfig().create_payment(grand_total, redirect_url)

    purchase = None
    if flutterwave:
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                payment_method=str(gateway_type),
                client_fee = int(total_gateway_fee),
                category = Purchase.PROPOSAL,
                salary_paid=grand_total,
                flutterwave_order_key=tx_ref,
                status = Purchase.FAILED
            )
        except Exception as e:
            print('%s' % (str(e)))

        try:
            for proposal in hiringbox:
                ProposalSale.objects.create(
                    package_name = proposal['package_name'],
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

        return JsonResponse({
            'tx_ref': tx_ref, 
            'amount': grand_total,
            'currency':base_currency,
            'redirect_url':'/transaction/flutter_success/',
            'email':request.user.email,
            'phone':request.user.phone,
            'customer':request.user.get_full_name(),
        })
    else:
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
                flutterwave_order_key=product['data']['tx_ref'], flutterwave_transaction_id=product['data']['id']
            )

            data = {"transaction_url": '/transaction/proposals/', "status": 'success',}
            hiringbox.clean_box()
            return JsonResponse(data)
        else:
            data = {"transaction_url": '.', "status": 'failed'}
            hiringbox.clean_box()
            return JsonResponse(data)
    else:
        data = {"transaction_url": '.', "status": 'failed'}
        return JsonResponse(data)


@login_required
@require_http_methods(['POST'])
def create_payment_intent(request):
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    gateway_type = str(hiringbox.get_gateway())
    
    card_token = request.POST.get('card_token')
    payment_id, client_secret = StripeClientConfig().create_payment_intent(grand_total, card_token)

    purchase = None
    if payment_id:
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                payment_method=str(gateway_type),
                client_fee = int(total_gateway_fee),
                category = Purchase.PROPOSAL,
                salary_paid=grand_total,
                stripe_order_key=payment_id,
                status = Purchase.FAILED
            )
        except Exception as e:
            print('%s' % (str(e)))

        try:
            for proposal in hiringbox:
                ProposalSale.objects.create(
                    package_name = proposal['package_name'],
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

        return JsonResponse({'client_secret': client_secret, 'payment_intent': payment_id})
    else:
        return JsonResponse({'client_secret': None})


@login_required
@require_http_methods(['POST'])
def stripe_payment_order(request):
    hiringbox = HiringBox(request)

    stripe_order_key = request.POST.get('stripe_order_key')
    Purchase.stripe_order_confirmation(stripe_order_key)
    hiringbox.clean_box()
    transaction_url = reverse('transactions:proposal_transaction') 
    return JsonResponse({'status': 'success', 'transaction_url':transaction_url})
    

@csrf_exempt
def stripe_webhook(request):
    pass
    # payload = request.body

    # stripe_obj = StripeClientConfig()
    # stripe.api_key = stripe_obj.stripe_secret_key()
    # webhook_key = stripe_obj.stripe_webhook_key()
    # sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # event = None
    # team = None
    # package = None
    
    # try:
    #     event = stripe.Webhook.construct_event(payload, sig_header, webhook_key)
    # except ValueError as e:
    #     return HttpResponse(status=400)
    # except stripe.error.SignatureVerificationError as e:
    #     return HttpResponse(status=400)

    # if event['type'] == 'checkout.session.completed':
    #     session = event['data']['object']
    #     if session.payment_status == 'paid':
    #         print('WEBHOOK', session.payment_intent)
    #         if session.mode == 'payment' and session['metadata']['mode'] == 'payment':
    #             try:
    #                 Purchase.stripe_order_confirmation(session.payment_intent)                    
    #             except Exception as e:
    #                 print('%s' % (str(e)))

    #         if session.mode == 'payment' and session['metadata']['mode'] == 'deposit':
    #             try:
    #                 deposit_fee = session['metadata']['deposit_fee']
    #                 deposit_gateway = session['metadata']['gateway']
    #                 narration = session['metadata']['narration']
    #                 amount_total = session.get('amount_total')
    #                 convert_fee = int(deposit_fee)
    #                 convert_amount = int(amount_total)
    #                 value_returned = int((convert_amount/100) - convert_fee)

    #                 ClientAccount.final_deposit(
    #                     user=session.get('client_reference_id'), 
    #                     amount=value_returned, 
    #                     deposit_fee=convert_fee, 
    #                     narration=narration, 
    #                     gateway=deposit_gateway
    #                 )                    
    #             except Exception as e:
    #                 print('%s' % (str(e)))

    #         if session.mode == 'subscription':
    #             try:                            
    #                 package = Package.objects.get(is_default=False, type='Team')
    #                 team = Team.objects.get(pk=session.get('client_reference_id'))
    #                 team.stripe_customer_id = session.get('customer')
    #                 team.stripe_subscription_id = session.get('subscription')
    #                 team.package = package
    #                 team.package_status = Team.ACTIVE
    #                 team.package_expiry = get_expiration()
    #                 team.save()   

    #             except Exception as e:
    #                 print('%s' % (str(e)))

    #             try:
    #                 SubscriptionItem.objects.create(    
    #                     team=team,
    #                     customer_id = team.stripe_customer_id,
    #                     subscription_id=team.stripe_subscription_id,
    #                     payment_method='Stripe', 
    #                     price=package.price, 
    #                     created_at = timezone.now(),
    #                     activation_time = timezone.now(),
    #                     expired_time = get_expiration(),
    #                     status = True,
    #                 )
                            
    #             except Exception as e:
    #                 print('%s' % (str(e)))
    #     else:
    #         print('Payment unsuccessful')  

    # return HttpResponse(status=200)


@login_required
def paypal_payment_order(request):
    hiringbox = HiringBox(request)
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    gateway_type = hiringbox.get_gateway()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    base_currency = str(get_base_currency_code()).lower()
    purchase = None

    PayPalClient = PayPalClientConfig()
    purchase = None

    paypal_order_key = PayPalClient.create_order(grand_total, base_currency)
    if paypal_order_key:
        try:
            purchase = Purchase.objects.create(
                client=request.user,
                payment_method=str(gateway_type),
                client_fee = int(total_gateway_fee),
                category = Purchase.PROPOSAL,
                salary_paid=grand_total,
                paypal_order_key=paypal_order_key,
                status = Purchase.FAILED
            )

        except Exception as e:
            print('%s' % (str(e)))
        
        try:
            for proposal in hiringbox:
                ProposalSale.objects.create(
                    package_name = proposal['package_name'],
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

        # hiringbox.clean_box()

        return JsonResponse({'paypal_order_key': paypal_order_key})
    else:
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
    gateway_type = hiringbox.get_gateway()
    base_currency_code = get_base_currency_code()
    total_gateway_fee = hiringbox.get_fee_payable()
    discount_value = hiringbox.get_discount_value()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()

    purchase = None
    razorpay_order_key = RazorpayClientConfig().create_order(grand_total)
    try:
        purchase = Purchase.objects.create(
            client=request.user,
            payment_method=str(gateway_type),
            client_fee = int(total_gateway_fee),
            category = Purchase.PROPOSAL,
            salary_paid=grand_total,
            razorpay_order_key=razorpay_order_key,
            status = Purchase.FAILED
        )
    except Exception as e:
        print('%s' % (str(e)))

    try:
        for proposal in hiringbox:
            ProposalSale.objects.create(
                package_name = proposal['package_name'],
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

    response = JsonResponse({'currency':base_currency_code, 'amount': (purchase.salary_paid), 'razorpay_order_key': purchase.razorpay_order_key})
    return response


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
    # transaction_url = reverse('transactions:proposal_transaction')

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

