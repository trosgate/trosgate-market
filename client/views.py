from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from .forms import ClientForm, AnnouncementForm
from django.contrib.auth import login
from account.models import Customer
from .models import Client, ClientAccount, ClientAction
from proposals.models import Proposal
from projects.models import Project
from django.http import JsonResponse
from django.urls import reverse
from account.permission import user_is_client
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from account.fund_exception import FundException
from payments.models import PaymentGateway
from paypalcheckoutsdk.orders import OrdersGetRequest
from general_settings.gateways import PayPalClientConfig, StripeClientConfig, FlutterwaveClientConfig, RazorpayClientConfig
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.fund_control import get_min_depositor_balance, get_max_depositor_balance, get_min_deposit, get_max_deposit
from django.contrib.sites.shortcuts import get_current_site
from transactions.models import Purchase
from contract.models import InternalContract, Contract
from control_settings.utilities import deposit_switch
import stripe
import json


@login_required
def client_profile(request, short_name):
    client = get_object_or_404(Client, user__short_name=short_name)
    client_staffs = client.employees.all().exclude(id=client.user.id)

    projects = Project.objects.filter(created_by=client.user, status=Project.ACTIVE)
    announcementform = AnnouncementForm()

    context = {
        'client': client,
        'projects': projects,
        'client_staffs': client_staffs,
        'announcementform': announcementform
    }
    return render(request, 'client/client_profile_detail.html', context)


@login_required
@user_is_client
def create_notice(request):
    client = get_object_or_404(Client, user=request.user)

    content = request.POST.get('content', '')
    if content != '' and len(content) <= 1000:
        client.announcement = content
        client.save()

    context = {
        'client':client,
    }       
    return render(request, 'client/partials/announcement.html', context)


@login_required
@user_is_client
def update_client(request, short_name):
    profile = get_object_or_404(Client, user__short_name=short_name, user=request.user)
    if request.method == 'POST':
        profileform = ClientForm(request.POST, request.FILES, instance=profile)

        if profileform.is_valid():
            profiles = profileform.save(commit=False)
            profiles.user = request.user

            profiles.save()
            profileform.save_m2m()  # for saving manytomany items in forms

            messages.info(request, 'Profile updated Successfully')

            return redirect("client:update_client_profile", short_name=profile.user.short_name)

    else:
        profileform = ClientForm(instance=profile)

    context = {
        'profileform': profileform,
        'profile': profile,
    }
    return render(request, 'client/client_profile_update.html', context)


def client_listing(request):
    client_profile_list = Client.objects.filter(user__is_active=True, user__user_type=Customer.CLIENT)
    context = {
        'client_profile_list': client_profile_list,
    }
    return render(request, 'client/client_listing.html', context)


@login_required
@user_is_client
def one_click_proposal_checkout(request):
    errors = ''
    err = ''
    message = ''
    if request.POST.get('action') == 'oneclick-pay':
        proposal_id = int(request.POST.get('proposalId'))
        
        proposal = get_object_or_404(Proposal, pk=proposal_id, status=Proposal.ACTIVE)
     
        if request.user.clientfunduser.available_balance >= proposal.salary:
            try:
                Purchase.one_click_proposal(user=request.user, proposal=proposal)
                message = f'<span id="oneClick-message" style="color:green; text-align:right;">"Congrats! Checkout Successful"</span>'
            except Exception as e:
                err = 'Error occured and we could not create order. Try again'
                errors = f'<span id="oneClick-error" style="color:red; text-align:right;">{err}</span>'
                print('%s' % (str(e)))
            return JsonResponse({'message':message, 'errors':errors})
        else:
            errors = f'<span id="oneClick-error" style="color:red; text-align:right;">Insufficient Balance to checkout</span>'
            return JsonResponse({'errors':errors})


@login_required
@user_is_client
def one_click_interncontract_checkout(request):
    errors = ''
    err = ''
    message = ''
    if request.POST.get('action') == 'oneclick-pay':
        contract_id = int(request.POST.get('contractId'))
        
        contract = get_object_or_404(InternalContract, pk=contract_id, created_by=request.user, reaction=InternalContract.ACCEPTED)
       
        if request.user.clientfunduser.available_balance >= contract.grand_total:
            try:
                Purchase.one_click_intern_contract(user=request.user, contract=contract)
                message = f'<span id="oneClick-message" style="color:green; text-align:right;">"Congrats! Checkout Successful"</span>'
            except FundException as e:
                err = str(e)
                errors = f'<span id="oneClick-error" style="color:red; text-align:right;">{err}</span>'
                print('%s' % (str(e)))
            return JsonResponse({'message':message, 'errors':errors})
        else:
            errors = f'<span id="oneClick-error" style="color:red; text-align:right;">Insufficient Balance to checkout</span>'
            return JsonResponse({'errors':errors})


@login_required
@user_is_client
def one_click_externcontract_checkout(request):
    errors = ''
    err = ''
    message = ''
    if request.POST.get('action') == 'oneclick-extpay':
        contract_id = int(request.POST.get('contractId'))
        
        contract = get_object_or_404(Contract, pk=contract_id, client__email=request.user.email, reaction=Contract.AWAITING)
    
        if request.user.clientfunduser.available_balance >= contract.grand_total:
            try:
                Purchase.one_click_extern_contract(user=request.user, contract=contract)
                message = f'<span id="oneClick-message" style="color:green; text-align:right;">"Congrats! Checkout Successful"</span>'
            except FundException as e:
                err = str(e)
                errors = f'<span id="oneClick-error" style="color:red; text-align:right;">{err}</span>'
                print('%s' % (str(e)))
            return JsonResponse({'message':message, 'errors':errors})
        else:
            errors = f'<span id="oneClick-error" style="color:red; text-align:right;">Insufficient Balance to checkout</span>'
            return JsonResponse({'errors':errors})


@login_required
@user_is_client
def deposit_fee_structure(request):
    client = get_object_or_404(Client, user=request.user, user__is_active=True)
    deposits = ClientAction.objects.filter(account__user = request.user)
    gateways = PaymentGateway.objects.filter(status=True).exclude(name='Balance')
    base_currency = get_base_currency_code()
    depo_switch = deposit_switch()
    context = {
        'client': client,
        'deposits': deposits,
        'gateways': gateways,
        'base_currency': base_currency,
        'depo_switch': depo_switch,
    }
    return render(request, 'client/deposit_step_one.html', context)


@login_required
@user_is_client
def deposit_fee_session(request):
    session = request.session
    if request.POST.get('action') == 'deposit-gateway':
        gateway_id = int(request.POST.get('depogateway'))
        gateway = PaymentGateway.objects.get(id=gateway_id, status=True)

        if "depositgateway" not in request.session:
            session["depositgateway"] = {"gateway_id": gateway.id}
            session.modified = True
        else:
            session["depositgateway"]["gateway_id"] = gateway.id
            session.modified = True

        context = {
            'gateway_fee': gateway.processing_fee 
        }

        response = JsonResponse(context)
        return response


@login_required
@user_is_client
def final_deposit(request):
    
    if "depositgateway" not in request.session:
        messages.error(request, "Please select deposit option to proceed")
        return redirect("client:deposit_fee_structure")

    stripe_public_key = ''
    paypal_public_key = ''
    flutterwave_public_key = ''
    razorpay_public_key = ''
    
    client = get_object_or_404(Client, user=request.user, user__is_active=True)    
    gateway_id = request.session["depositgateway"]["gateway_id"]
    selected_gateway = PaymentGateway.objects.get(pk=gateway_id, status=True)

    # Stripe payment api
    if selected_gateway.name =="Stripe":
        stripe_public_key = StripeClientConfig().stripe_public_key()
    # Paypal payment api
    if selected_gateway.name =="PayPal":
        paypal_public_key = PayPalClientConfig().paypal_public_key()
    # Futterwave payment api
    if selected_gateway.name =="Flutterwave":
        flutterwave_public_key = FlutterwaveClientConfig().flutterwave_public_key()
    # Razorpay payment api
    if selected_gateway.name =="Razorpay":
        razorpay_public_key = RazorpayClientConfig().razorpay_public_key_id()

    # base_currency = get_base_currency_code()
    min_depositor_balance = get_min_depositor_balance()
    max_depositor_balance = get_max_depositor_balance()
    min_deposit = get_min_deposit()
    max_deposit = get_max_deposit()
    base_currency = get_base_currency_symbol()
    base_currency_code = get_base_currency_code()

    context = {
        "client": client,
        "paypal_public_key": paypal_public_key,
        "stripe_public_key": stripe_public_key,
        "flutterwave_public_key": flutterwave_public_key,
        "razorpay_public_key": razorpay_public_key,
        "base_currency_code": base_currency_code,
        "base_currency": base_currency,
        "paypal_public_key": paypal_public_key,
        "selected_gateway": selected_gateway,
        'min_depositor_balance': min_depositor_balance,
        'max_depositor_balance': max_depositor_balance,
        'min_deposit': min_deposit,
        'max_deposit': max_deposit,                
    }

    return render(request, 'client/deposit_step_final.html', context)


@login_required
@user_is_client
def stripe_deposit(request):
    message = ''
    data = json.loads(request.body)
    gateway_id = request.session["depositgateway"]["gateway_id"]
    selected_gateway = PaymentGateway.objects.get(pk=gateway_id, status=True)

    deposit_amount = data['stripeAmount']
    narration = data['stripeNarration']
    amount_to_str = int(deposit_amount)
    deposit_fee = selected_gateway.processing_fee
    total_amount = int((amount_to_str + deposit_fee) * 100)

    stripe_obj = StripeClientConfig()
    stripe.api_key = stripe_obj.stripe_secret_key()

    try:
        ClientAccount.deposit_check(
            user=request.user, deposit_amount=total_amount, narration=narration
        )

    except FundException as e:
        message = str(e)

    session = stripe.checkout.Session.create(
        client_reference_id=request.user.id,
        customer_email = request.user.email,        
        metadata = {
            'mode':'deposit', 
            'gateway':selected_gateway.name, 
            'deposit_fee':deposit_fee, 
            'narration':narration
        },
        payment_method_types=['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': narration,
                    },
                    'unit_amount': total_amount,
                },
                'quantity': 1
            },
        ],
        mode='payment',
        success_url='http://' + str(get_current_site(request)) + '/client/congrats/',
        cancel_url='http://' + str(get_current_site(request)) + '/dashboard/'
    )

    print('sessionId', session)
    payment_intent = session.payment_intent

    # del request.session["depositgateway"]
    # del request.session["acceptdepoamount"]
    return JsonResponse({'session':session, 'order':payment_intent, 'message':message}, safe=False)


@login_required
def razor_deposit_checker(request):
    razorpay_api = RazorpayClientConfig()

    gateway_id = request.session["depositgateway"]["gateway_id"]
    selected_gateway = PaymentGateway.objects.get(pk=gateway_id, status=True)
    
    message = ''
    razorpay_order = ''
    total_amount = ''
    narration = ''

    notes = {'Total Price': 'The total amount may change with discount'}
    currency = get_base_currency_code()
    razorpay_client = razorpay_api.get_razorpay_client()

    if request.POST.get('action') == 'razorpay-deposit':
        amount = int((request.POST.get('razordepositAmount')))
        narration = str(request.POST.get('razordepositNarration'))
        deposit_fee = selected_gateway.processing_fee
        total_amount = int((amount + deposit_fee) * 100)

        try:
            ClientAccount.deposit_check(
                user=request.user, deposit_amount=amount, narration=narration
            )

        except FundException as e:
            message = str(e)

        try:
            razorpay_order = razorpay_client.order.create(dict(
                amount = total_amount, 
                currency = currency, 
                notes = notes, 
            ))

        except FundException as e:
            message = str(e)

        if "acceptdepoamount" not in request.session:
            request.session["acceptdepoamount"] = {"acceptdeposit_amount": amount}
            request.session.modified = True

        return JsonResponse({'total_amount':total_amount, 'message':message, 'razorpay_order_id': str(razorpay_order['id'])}, safe=False)


def razorpay_callback(request):
    razorpay_api = RazorpayClientConfig()
    razorpay_client = razorpay_api.get_razorpay_client()

    gateway_id = int(request.session["depositgateway"]["gateway_id"])
    deposit_amount = int(request.session["acceptdepoamount"]['acceptdeposit_amount'])

    selected_gateway = PaymentGateway.objects.get(pk=gateway_id, status=True)
    deposit_fee = int(selected_gateway.processing_fee)

    if request.POST.get('action') == 'razorpay-deposit-confirm':
        narration = str(request.POST.get('razordepositNarration'))
        razorpay_payment_id = str(request.POST.get('razorpay_payment_id'))    
        razorpay_order_id = str(request.POST.get('razorpay_order_id'))    
        razorpay_signature = str(request.POST.get('razorpay_signature'))
        total_amount = int(request.POST.get('total_amount'))

        data ={
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        signature = razorpay_client.utility.verify_payment_signature(data)

        new_total_amount = total_amount/100
        original_amount = int(new_total_amount) - int(deposit_fee)


        if original_amount == deposit_amount:
            print(';all matched ;all matched ;all matched')

        if signature == True:
            ClientAccount.final_deposit(
                user=request.user, 
                amount=int(original_amount), 
                deposit_fee=deposit_fee, 
                narration=narration, 
                gateway=str(selected_gateway)
            )
        
            del request.session["depositgateway"]
            del request.session["acceptdepoamount"]

            return JsonResponse({'perfect':'perfect'}, safe=False)


# level_two_deposit_check
@login_required
def payment_success(request):
    # hiringbox = HiringBox(request)
    # hiringbox.clean_box()

    context = {
        "good": "good"
    }
    return render(request, "transactions/payment_success.html", context)
