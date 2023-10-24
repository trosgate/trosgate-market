import json
import stripe
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContractorForm, InternalContractForm, ExternalContractForm
from .models import Contractor, Contract, ContractChat
from payments.models import PaymentGateway
from account.models import Customer
from teams.models import Team
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.permission import user_is_freelancer, user_is_client
from freelancer.models import Freelancer
from client.models import Client
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .contract import BaseContract
from django.views.decorators.csrf import csrf_exempt
from transactions.models import Purchase, ContractSale
from transactions.utilities import get_base_currency, calculate_contract_payment_data
from paypalcheckoutsdk.orders import OrdersGetRequest
from payments.paypal import PayPalClientConfig
from payments.stripe import StripeClientConfig
from payments.razorpay import RazorpayClientConfig
from payments.flutterwave import FlutterwaveClientConfig
from payments.paystack import PaystackClientConfig
from general_settings.discount import get_discount_calculator, get_earning_calculator
from general_settings.fees_and_charges import get_contract_fee_calculator
from general_settings.forms import CurrencyForm
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.cache import cache_control
from general_settings.utilities import get_protocol_only
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.cache import never_cache
from .utilities import permit_client, can_accept_or_reject


@login_required
@user_is_freelancer
def add_contractor(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    contractors = team.contractors.all()
    contractorform = ContractorForm(request.POST or None)
    if request.method == 'POST':
        if contractorform.is_valid():
            name = contractorform.cleaned_data['name']
            email = contractorform.cleaned_data['email']
            try:
                Contractor.add_client(
                    name=name,email=email,team=team,created_by=request.user
                )
                messages.info(request, f'Client added successfully')
            except Exception as e:
                messages.error(request, f'{e}!')
        else:
            messages.error(request, f'Invalid name or email!')
        context={
            'contractors': contractors,
            # 'contractorform': ContractorForm()
        }
        return render(request, 'contract/components/contract.html', context)
    else:
        context={
            'contractorform': ContractorForm(),
            'contractors': contractors
        }
        return render(request, 'contract/components/contract.html', context)


@login_required
@user_is_freelancer
def delete_contractor(request, contractor_id):
    team = get_object_or_404(
        Team, 
        pk=request.user.freelancer.active_team_id, 
        members__in=[request.user], 
        status=Team.ACTIVE
    )
    contractors = Contractor.objects.filter(team=team)    
    contractor = get_object_or_404(Contractor, team=team, pk=contractor_id)

    if Customer.objects.filter(email = contractor.email).exists():
        messages.error(request, 'You cannot delete client. Client either join site or paid for the connected contract!')
    else:
        contractor.delete()

    context={
        'contractors': contractors
    }
    return render(request, 'contract/components/contract.html',context)


@login_required
@user_is_freelancer
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_external_contract(request, reference):
    team = get_object_or_404(Team,pk=request.user.freelancer.active_team_id,status=Team.ACTIVE)
    client = get_object_or_404(Contractor, pk=reference, team=team)
    existing_user = Customer.objects.filter(email=client.email).count()
    existing_contract = Contract.objects.filter(client__email=client.email).count()
    
    profile_path= f"{get_protocol_only()}{str(get_current_site(request))}/freelancer/profile/{request.user.short_name}/"
    base_currency = get_base_currency(request)
    
    if request.method == 'POST':
        contractform = ExternalContractForm(request.POST or None)

        if contractform.is_valid():
            contract = contractform.save(commit=False)
            contract.created_by = request.user
            contract.team = team
            contract.contract_type = Contract.EXTERNAL
            contract.client = client
            contract.slug = slugify(contract.line_one)
            contract.save()

            messages.info(request, 'The contract was added!')
            return redirect('contract:contract_list')

    else:
        contractform = ExternalContractForm()
    context = {
        'contractform': contractform,
        'team': team,
        'client': client,
        'base_currency': base_currency,
        'existing_user': existing_user,
        'existing_contract': existing_contract,
        'profile_path': profile_path
    }
    return render(request, 'contract/connect_contract.html', context)


@login_required
@user_is_client
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_internal_contract(request, short_name):
    freelancer = get_object_or_404(Freelancer, user__short_name=short_name)
    team = get_object_or_404(Team, pk=freelancer.active_team_id, status=Team.ACTIVE)
    monthly_contracts_limiter = team.monthly_contract_slot
    
    if request.method == 'POST':
        intcontractform = InternalContractForm(team, request.POST)

        if intcontractform.is_valid():
            contract = intcontractform.save(commit=False)
            contract.created_by = request.user
            contract.contract_type = Contract.INTERNAL
            contract.team = contract.proposal.team
            contract.slug = slugify(contract.proposal.title)
            contract.save()

            messages.success(request, 'The contract was added successfully!')
            return redirect('freelancer:freelancer_listing')

    else:
        intcontractform = InternalContractForm(team)
    context = {
        'freelancer': freelancer,
        'team': team,
        'intcontractform': intcontractform,
        'monthly_contracts_limiter': monthly_contracts_limiter,
    }
    return render(request, 'contract/add_internal_contract.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def contract_list(request):
    team = None
    contractors = None
    contracts = None
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id)
        contractors = team.contractors.all()
        contracts = team.contracts.all()

    elif request.user.user_type == Customer.CLIENT:
        contracts = Contract.objects.filter(
            Q(created_by=request.user)|
            Q(client__email__iexact=request.user.email)
        ).select_related('client', 'proposal')
    else:
        contracts = Contract.objects.filter(
            merchant__merchant=request.user
        )

    context = {
        'team': team,
        'contractors': contractors,
        'contracts': contracts,
    }
    return render(request, 'contract/contract.html', context)


@login_required
def contract_detail(request, identifier, contract_slug):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
        contract = get_object_or_404(Contract, team=team, identifier=identifier, slug=contract_slug)

    if request.user.user_type == Customer.CLIENT:
        contract = get_object_or_404(Contract, identifier=identifier, slug=contract_slug)
        user_is_client = permit_client(request, contract)
        if not user_is_client:
            return HttpResponseNotFound()
            
    if request.user.user_type == Customer.MERCHANT:
        contract = get_object_or_404(Contract, identifier=identifier, slug=contract_slug, merchant__merchant=request.user)

    context = {
        "contract": contract,
    }
    return render(request, 'contract/contract_detail.html', context)


@login_required
def accept_or_reject_contract(request):
    contract_id = request.POST.get('contractid')
    contract = get_object_or_404(Contract, id=contract_id)

    activator = can_accept_or_reject(contract)
    if not activator:
        return HttpResponseNotFound()
        
    if request.POST.get('action') == 'accept':
        contract = Contract.capture(contract.id, contract.ACCEPTED)

    elif request.POST.get('action') == 'reject':
        contract = Contract.capture(contract.id, contract.REJECTED)

    else:
        messages.error(request, 'No option selected')

    context = {
        "contract": contract,
    }
    return render(request, 'contract/components/accept_or_reject.html', context)


@login_required
def refresh_contract(request):
    contract_id = request.GET.get('refresh')
    contract = Contract.objects.filter(id=contract_id).first()
    message = 'No action taken on this contract.'

    if contract is not None and contract.reaction != 'awaiting':
        message = 'Action taken on Contract'

    messages.info(request, f'{message}')
    context = {
        "contract": contract,
    }
    return render(request, 'contract/components/accept_or_reject.html', context)


@login_required
def pricing_option_with_fees(request, identifier):
    base_contract = BaseContract(request)
    payment_gateways = request.merchant.gateways.all().exclude(name='balance')
    contract = get_object_or_404(Contract, identifier=identifier, reaction=Contract.ACCEPTED)
    
    user_is_client = permit_client(request, contract)
    if not user_is_client:
        return HttpResponseNotFound()
    
    payment_data = calculate_contract_payment_data(base_contract, contract)
    base_currency = get_base_currency(request)

    if request.method == 'POST':
        gateways = int(request.POST.get('paymentGateway'))
        gateway = PaymentGateway.objects.filter(id=gateways).first()

        session = request.session

        if gateway:
            
            if "contractgateway" not in session:
                session["contractgateway"] = {"gateway_id": gateway.id}
                session.modified = True
            else:
                session["contractgateway"]["gateway_id"] = gateway.id
                session.modified = True
        else:
            pass
        
        payment_data = calculate_contract_payment_data(base_contract, contract)

    context ={
        'contract': contract,
        'selected': 'selected',
        'payment_gateways': payment_gateways,
        'base_currency': base_currency,
        'payment_method': 'Payment Summary',
        "discount": payment_data['discount_value'],
        'subtotal': payment_data['grand_total_before_expense'],
        'grand_total': payment_data['grand_total'],
        'selected_fee': payment_data['total_gateway_fee'],
        "gateway_type": payment_data['gateway_type'].lower(),
    }
    if request.htmx:
        return render(request, "contract/components/pricing_option_with_fees.html", context)

    return render(request, "contract/pricing_option_with_fees.html", context)


@login_required
@user_is_client
def final_contract_checkout(request, identifier, contract_slug):
    base_contract = BaseContract(request)
    contract = get_object_or_404(Contract, identifier=identifier, slug=contract_slug, reaction=Contract.ACCEPTED)
    session = request.session
    
    user_is_client = permit_client(request, contract)
    if not user_is_client:
        return HttpResponseNotFound()

    if "contractgateway" not in session:
        messages.error(request, "Please select payment option to proceed")
        return redirect("contract:pricing_option_with_fees", contract_id=contract.identifier)

    base_contract.capture(contract = contract)
    payment_data = calculate_contract_payment_data(base_contract, contract)
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
    return render(request, "contract/final_contract_checkout.html", context)


@login_required
@never_cache
@require_http_methods(['POST'])
def stripe_payment_intent(request):
    base_contract = BaseContract(request)
    contract_id = request.session["chosencontract"]["contract_id"]
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED)
    payment_data = calculate_contract_payment_data(base_contract, contract)

    card_token = request.POST.get('card_token')
    stripe_client = StripeClientConfig()
    payment_id, client_secret = stripe_client.create_payment_intent(contract.grand_total, card_token)

    purchase = None
    try:
        purchase = Purchase.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.CONTRACT,
            stripe_order_key=payment_id,
            hiringbox=base_contract,
            contract=contract
        )
        response_data = {
            'client_secret': client_secret,
            'payment_intent': purchase.stripe_order_key,
        }
        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'status': 'failed'})


@login_required
@never_cache
@require_http_methods(['POST'])
def stripe_payment_order(request):
    applicant_box = BaseContract(request)
    stripe_order_key = request.POST.get('stripe_order_key')
    Purchase.stripe_order_confirmation(stripe_order_key)
    applicant_box.clean_box()
    transaction_url = reverse('transactions:contract_transaction')
    return JsonResponse({'status': 'success', 'transaction_url':transaction_url})


@login_required
@never_cache
@user_is_client
def flutter_payment_intent(request):
    base_contract = BaseContract(request)
    contract_id = request.session["chosencontract"]["contract_id"]
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED)
    payment_data = calculate_contract_payment_data(base_contract, contract)
    base_currency = get_base_currency(request)
    
    purchase = None
    try:
        purchase = Purchase.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.CONTRACT,
            hiringbox=base_contract,
            contract=contract
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
@never_cache
@require_http_methods(['GET'])
def flutter_success(request):
    base_contract = BaseContract(request)
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

            base_contract.clean_box()
            data = {"status": "success", 'redirect_url':'/contract/flutter_success/'}
            return JsonResponse(data)
        else:
            data = {"status": 'failed'}
            return JsonResponse(data)
    else:
        data = {"status": 'failed'}
        return JsonResponse(data)


@login_required
@never_cache
@require_http_methods(['GET'])
def paypal_payment_order(request):
    base_contract = BaseContract(request)
    contract_id = request.session["chosencontract"]["contract_id"]
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED)
    payment_data = calculate_contract_payment_data(base_contract, contract)
    purchase = None
    paypal_order_key = PayPalClientConfig().create_order(contract.grand_total)
    if paypal_order_key:
        try:
            purchase = Purchase.create_purchase_and_sales(
                client=request.user,
                **payment_data,
                category=Purchase.CONTRACT,
                paypal_order_key=paypal_order_key,
                hiringbox=base_contract,
                contract=contract
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


@csrf_exempt
@never_cache
@require_http_methods(['POST'])
def paypal_callback(request):
    base_contract = BaseContract(request)
    body = json.loads(request.body)
    paypal_order_key = body["paypal_order_key"]

    capture_data = PayPalClientConfig().capture_order(paypal_order_key)
    capture_data_id = capture_data['purchase_units'][0]['payments']['captures'][0]['id']
    if capture_data['status'] == 'COMPLETED':
        Purchase.paypal_order_confirmation(paypal_order_key, capture_data_id)
        base_contract.clean_box()
        return JsonResponse(capture_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@login_required
@user_is_client
@never_cache
def paystack_payment_intent(request):
    base_contract = BaseContract(request)
    contract_id = request.session["chosencontract"]["contract_id"]
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED)
    payment_data = calculate_contract_payment_data(base_contract, contract)
    base_currency = get_base_currency(request)

    purchase = None
    try:
        purchase = Purchase.create_purchase_and_sales(
            client=request.user,
            **payment_data,
            category=Purchase.CONTRACT,
            hiringbox=base_contract,
            contract=contract
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
@never_cache
def paystack_callback(request):
    base_contract = BaseContract(request)      
    payment_reference = request.POST.get('payment_reference')
    transaction_id = request.POST.get('transaction_reference')
    message = request.POST.get('message')
    status = request.POST.get('status')

    try:
        
        if status == 'success' and message == 'Approved':
            Purchase.paystack_order_confirmation(
                payment_reference, transaction_id
            )
            base_contract.clean_box()
            return JsonResponse({
                'status': 'success', 
                'transaction_url': '/transaction/contract/'}
            )
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
  

@login_required
@never_cache
@user_is_client
def razorpay_contract_intent(request):
    base_contract = BaseContract(request)
    contract_id = request.session["chosencontract"]["contract_id"]
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED)
    payment_data = calculate_contract_payment_data(base_contract, contract)
    base_currency = get_base_currency(request)
    
    purchase = None
    
    razorpay_order_key = RazorpayClientConfig().create_order(contract.grand_total)
    if razorpay_order_key:
        try:
            purchase = Purchase.create_purchase_and_sales(
                client=request.user,
                **payment_data,
                category=Purchase.CONTRACT,
                razorpay_order_key=razorpay_order_key,
                hiringbox=base_contract,
                contract=contract
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
@never_cache
@user_is_client
def razorpay_callback(request):
    base_contract = BaseContract(request)    
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
            base_contract.clean_box()
            return JsonResponse({'status':'success','transaction_url':'/transaction/contract/'})
        except Exception as e:
            print('%s' % (str(e)))
            return JsonResponse({'status':'error'}) 

    else:
        return JsonResponse({'status':'error'})


@login_required
# same contract can be applied many times so add contract ID to params --TODO
def contract_chat(request, contract_id, contract_slug):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
        contract = get_object_or_404(Contract, pk=contract_id, slug=contract_slug, team=team)

    elif request.user.user_type == Customer.CLIENT:
        contract = get_object_or_404(Contract, pk=contract_id, slug=contract_slug, created_by=request.user)

    chats = ContractChat.objects.all()
    return render(request, 'contract/contract_chat.html', {'chats': chats, 'contract': contract})


@login_required
def create_contract_chat(request,  contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    
    content = request.POST.get('content', '')
    if content != '':
        ContractChat.objects.create(content=content, contract=contract, team=contract.team, sender=request.user)
    
    chats = ContractChat.objects.filter(contract=contract, team=contract.team)   
    return render(request, 'contract/components/partial_contract_message.html', {'chats': chats})


@login_required
def fetch_messages(request,  contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    chats = ContractChat.objects.filter(contract=contract, team=contract.team)   
    return render(request, 'contract/components/partial_contract_message.html', {'chats': chats})


