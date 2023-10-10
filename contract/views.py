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


@login_required
def contract_detail(request, identifier, contract_slug):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
        contract = get_object_or_404(Contract, team=team, identifier=identifier, slug=contract_slug)

    if request.user.user_type == Customer.CLIENT:
        contract = get_object_or_404(Contract, identifier=identifier, slug=contract_slug)
        if contract.contract_type == Contract.INTERNAL:
            user_is_client = request.user == contract.created_by
        else:
            user_is_client = request.user.email == contract.client.email
        
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

    if contract.contract_type == Contract.INTERNAL:
        activator = contract.team.created_by
    else:
        activator = contract.client
    
    if activator:
        if request.POST.get('action') == 'accept':
            contract = Contract.capture(contract.id, contract.ACCEPTED)

        elif request.POST.get('action') == 'reject':
            contract = Contract.capture(contract.id, contract.REJECTED)

        else:
            messages.error(request, 'No option selected')
    else:
        raise HttpResponseNotFound()

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
def pricing_option_with_fees(request, contract_id, contract_slug):
    base_contract = BaseContract(request)
    payment_gateways = request.merchant.gateways.all().exclude(name='balance')
    contract = get_object_or_404(Contract, pk=contract_id, slug=contract_slug, reaction=Contract.ACCEPTED)
    
    if contract.contract_type == Contract.INTERNAL:
        user_is_client = request.user == contract.created_by
    else:
        user_is_client = request.user.email == contract.client.email
    
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
        "gateway_type": payment_data['gateway_type'],
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
    
    if contract.contract_type == Contract.INTERNAL:
        user_is_authorized = request.user == contract.created_by
    else:
        user_is_authorized = request.user.email == contract.client.email
    
    if not user_is_authorized:
        return HttpResponseNotFound()

    if "contractgateway" not in session:
        messages.error(request, "Please select payment option to proceed")
        return redirect("contract:pricing_option_with_fees", contract_id=contract.id, contract_slug=contract.slug)

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
@require_http_methods(['POST'])
def stripe_payment_order(request):
    applicant_box = BaseContract(request)
    stripe_order_key = request.POST.get('stripe_order_key')
    Purchase.stripe_order_confirmation(stripe_order_key)
    applicant_box.clean_box()
    transaction_url = reverse('transactions:contract_transaction')
    return JsonResponse({'status': 'success', 'transaction_url':transaction_url})


@login_required
@user_is_client
def flutter_payment_intent(request):
    contract_id = request.session["contractchosen"]["contract_id"]
    chosen_contract = BaseContract(request)
    gateway_type = str(chosen_contract.get_gateway())
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED, created_by=request.user)
    
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)  
    grand_total = chosen_contract.get_total_price_after_discount_and_fee(contract)
    purchase = None

    base_currency = get_base_currency(request)
    flutterwaveClient = FlutterwaveClientConfig()
    unique_reference = flutterwaveClient.flutterwave_unique_reference()

    if Purchase.objects.filter(unique_reference=unique_reference).exists():
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
                category = Purchase.CONTRACT,
                salary_paid=grand_total,
                unique_reference=unique_reference,           
            )           
            purchase.status=Purchase.FAILED
            purchase.save()
        except Exception as e:
            print('%s' % (str(e)))

        try:
            ContractSale.objects.create(
                team=contract.team, 
                purchase=purchase,  
                contract=contract, 
                sales_price=contract.grand_total,  
                staff_hired=int(1),
                earning_fee_charged=int(get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),                   
                total_earning_fee_charged=int(get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),                   
                discount_offered=get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value),
                total_discount_offered=get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value),
                disc_sales_price=int(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value)),
                total_sales_price=int((contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                earning=int(get_earning_calculator(
                    (contract.grand_total - (get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                    get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (contract.grand_total - (get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                    get_contract_fee_calculator(contract.grand_total- get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))))         
            
            )
        except Exception as e:
            print('%s' % (str(e)))

    redirect_url= f"{get_protocol_only()}{str(get_current_site(request))}/contract/flutter-success/",
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


@login_required
@user_is_client
@require_http_methods(['GET', 'POST'])
def flutter_contract_success(request):
    chosen_contract = BaseContract(request)
    status = request.GET.get('status', None)
    unique_reference = request.GET.get('tx_ref', '')
    flutterwave_order_key = request.GET.get('transaction_id', '')
    message = ''
    if status == 'successful' and unique_reference != '' and flutterwave_order_key != '':
        Purchase.flutterwave_order_confirmation(
            unique_reference=unique_reference, 
            flutterwave_order_key=flutterwave_order_key
        )
        message = 'Payment succeeded'
    else:
        message = 'Payment failed'
        return HttpResponse(status=401)
       
    chosen_contract.clean_box()
    context = {
        "good": message
    }
    return render(request, "contract/payment_success.html", context)


@login_required
@user_is_client
def paypal_contract_intent(request):
    chosen_contract = BaseContract(request)
    contract_id = request.session["contractchosen"]["contract_id"]
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED, created_by=request.user)
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    gateway_type = chosen_contract.get_gateway()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)
 
    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)
    data = body["orderID"]

    purchase = None
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
                category = Purchase.CONTRACT,
                salary_paid=round(float(response.result.purchase_units[0].amount.value)),
                paypal_order_key=response.result.id,
                unique_reference=PayPalClient.paypal_unique_reference(),
                status = Purchase.FAILED
            )
        except Exception as e:
            print('%s' % (str(e)))

        try:
            ContractSale.objects.create(
                team=contract.team, 
                purchase=purchase,  
                contract=contract, 
                sales_price=contract.grand_total, 
                staff_hired=int(1),
                earning_fee_charged=int(get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),                   
                total_earning_fee_charged=int(get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),                   
                discount_offered=get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value),
                total_discount_offered=get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value),
                disc_sales_price=int(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value)),
                total_sales_price=int((contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                earning=int(get_earning_calculator(
                    (contract.grand_total - (get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                    get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (contract.grand_total - (get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                    get_contract_fee_calculator(contract.grand_total- get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))))         
            
            )
        except Exception as e:
            print('%s' % (str(e)))

        try:
            Purchase.paypal_order_confirmation(pk=purchase.pk)
        except Exception as e:
            print('%s' % (str(e)))  

        chosen_contract.clean_box()
        return JsonResponse({'Perfect':'All was successful',})

    else:
        purchase.status = Purchase.FAILED
        purchase.save()
        return JsonResponse({'failed':'Transaction failed, Razorpay will refund your money if you are already debited',})
                

@login_required
@user_is_client
def razorpay_contract_intent(request):
    contract_id = request.session["contractchosen"]["contract_id"]
    chosen_contract = BaseContract(request)
    gateway_type = chosen_contract.get_gateway()
    total_gateway_fee = int(chosen_contract.get_fee_payable())
    contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED, created_by=request.user)   
    
    grand_total = chosen_contract.get_total_price_after_discount_and_fee(contract)
    gateway_type = str(chosen_contract.get_gateway())
    # base_currency_code = get_base_currency()
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)       
    
    razorpay_api = RazorpayClientConfig()
    unique_reference = razorpay_api.razorpay_unique_reference()
    try:
        purchase = Purchase.objects.create(
            client=request.user,
            full_name=request.user.get_full_name,
            email=request.user.email,
            country=str(request.user.country),
            payment_method=gateway_type,
            client_fee = total_gateway_fee,
            category = Purchase.CONTRACT,
            salary_paid=grand_total,
            unique_reference=unique_reference,
            status = Purchase.FAILED 
        )
    except Exception as e:
        print('%s' % (str(e)))

    try:
        ContractSale.objects.create(
            team=contract.team, 
            purchase=purchase,  
            contract=contract, 
            sales_price=contract.grand_total, 
            staff_hired=int(1),
            earning_fee_charged=int(get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),                   
            total_earning_fee_charged=int(get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),                 
            discount_offered=get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value),
            total_discount_offered=get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value),
            disc_sales_price=int(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value)),
            total_sales_price=int((contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
            earning=int(get_earning_calculator(
                (contract.grand_total - (get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                get_contract_fee_calculator(contract.grand_total - get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value)))), 
            total_earning=int(get_earning_calculator(
                (contract.grand_total - (get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))),
                get_contract_fee_calculator(contract.grand_total- get_discount_calculator(contract.grand_total, grand_total_before_expense, discount_value))))         
        
        )
    except Exception as e:
        print('%s' % (str(e)))

    notes = {'Total Price': 'The total amount may change with discount'}

    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_order = razorpay_client.order.create(dict(
        amount = int(grand_total * 100), 
        # currency = currency, 
        notes = notes, 
        receipt = purchase.unique_reference
    ))

    purchase.razorpay_order_key = razorpay_order['id']
    purchase.save()

    response = JsonResponse({'contract':contract.id, 'currency':currency, 'amount': (purchase.salary_paid), 'razorpay_order_key': purchase.razorpay_order_key})
    return response


@login_required
@user_is_client
def razorpay_webhook(request):
    chosen_contract = BaseContract(request)
    razorpay_client = RazorpayClientConfig().get_razorpay_client()
    if request.POST.get('action') == 'razorpay-contract':   
        razorpay_order_key = str(request.POST.get('orderid'))
        razorpay_payment_id = str(request.POST.get('paymentid'))
        razorpay_signature = str(request.POST.get('signature'))

        data ={
            'razorpay_order_id': razorpay_order_key,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }    
        signature = razorpay_client.utility.verify_payment_signature(data)

        if signature == True:
            try:
                Purchase.razorpay_order_confirmation(razorpay_order_key, razorpay_payment_id, razorpay_signature)
                chosen_contract.clean_box()
                return JsonResponse({'Perfect':'All was successful',})
            except Exception as e:
                print('%s' % (str(e))) 

        else:
            return JsonResponse({'failed':'Transaction failed, Razorpay will refund your money if you are already debited',})
   

@login_required
@user_is_client
def contract_success(request):

    context = {
        "good": "All good"
    }
    return render(request, "contract/payment_success.html", context)


@login_required
@user_is_client
def external_contract_fee_structure(request, contract_id, contract_slug):
    payment_gateways = PaymentGateway.objects.filter(status=True).exclude(name='balance')
    contract = get_object_or_404(Contract, pk=contract_id, slug=contract_slug, reaction=Contract.ACCEPTED, client__email=request.user.email)
    base_currency = get_base_currency(request)
    context = {
        "contract": contract,
        "base_currency": base_currency,
        "payment_gateways": payment_gateways,
    }
    return render(request, 'contract/external_fee_structure.html', context)


@login_required
@user_is_client
def external_contract_fee_selection(request):
    session = request.session
    gateway = None
    if request.POST.get('action') == 'capture-extcontract':
        contract_id = int(request.POST.get('contractid'))
        gateway_type = int(request.POST.get('gatewaytype'))
        contract = get_object_or_404(Contract, pk=contract_id, reaction=Contract.ACCEPTED, client__email=request.user.email)

        if "externcontractchosen" not in request.session:
            session["externcontractchosen"] = {"contract_id": contract.id}
            session.modified = True
        try:
            gateway = PaymentGateway.objects.get(id=gateway_type)
        except:
            gateway = None

        if "externcontractgateway" not in request.session:
            session["externcontractgateway"] = {"gateway_id": gateway.id}
            session.modified = True
        else:
            session["externcontractgateway"]["gateway_id"] = gateway.id
            session.modified = True

        context = {
            'contract_fee': gateway.processing_fee,
        }

        response = JsonResponse(context)
        return response


@login_required
@user_is_client
def contract_success(request):

    context = {
        "good": "All good"
    }
    return render(request, "contract/payment_success.html", context)


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


