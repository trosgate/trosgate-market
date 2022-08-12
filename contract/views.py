import json
import stripe
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContractorForm, InternalContractForm, ExternalContractForm, ChangeContractorForm
from .models import Contractor, Contract, InternalContract, ContractChat
from general_settings.models import PaymentGateway
from account.models import Customer
from proposals.models import Proposal
from teams.models import Team
from django.utils.text import slugify
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from account.permission import user_is_freelancer, user_is_client
from freelancer.models import Freelancer
from client.models import Client
from django.http import HttpResponse, JsonResponse
from .contract import BaseContract
from django.views.decorators.csrf import csrf_exempt
from transactions.models import Purchase, ContractSale
from paypalcheckoutsdk.orders import OrdersGetRequest
from general_settings.gateways import PayPalClientConfig, StripeClientConfig, FlutterwaveClientConfig, RazorpayClientConfig
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.discount import get_discount_calculator, get_earning_calculator
from general_settings.fees_and_charges import get_contract_fee_calculator
from general_settings.models import PaymentGateway
from general_settings.forms import CurrencyForm
from django.contrib.sites.shortcuts import get_current_site
from teams.controller import PackageController
from notification.mailer import send_contract_accepted_email, send_contract_rejected_email

# <...........................................................Internal Contract Section..........................................................>


@login_required
@user_is_client
def create_internal_contract(request, short_name):
    freelancer = get_object_or_404(Freelancer, user__short_name=short_name)
    team = get_object_or_404(Team, pk=freelancer.active_team_id, status=Team.ACTIVE)
    monthly_contracts_limiter = PackageController(team).monthly_offer_contracts()
     
    if request.method == 'POST':
        intcontractform = InternalContractForm(team, request.POST)

        if intcontractform.is_valid():
            contract = intcontractform.save(commit=False)
            contract.created_by = request.user
            contract.team = contract.proposal.team
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
def internal_contract_list(request):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
        intcontracts = team.internalcontractteam.all()
    elif request.user.user_type == Customer.CLIENT:
        intcontracts = InternalContract.objects.filter(created_by=request.user)
    context = {
        "intcontracts": intcontracts,
    }
    return render(request, 'contract/internal_contract_list.html', context)


@login_required
def internal_contract_detail(request, contract_id, contract_slug):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
        contract = get_object_or_404(InternalContract, team=team, pk=contract_id, slug=contract_slug)

    elif request.user.user_type == Customer.CLIENT:
        contract = get_object_or_404(InternalContract, pk=contract_id, slug=contract_slug, created_by=request.user)

    context = {
        "contract": contract,
    }
    return render(request, 'contract/internal_contract_detail.html', context)



@login_required
@user_is_freelancer
def accept_or_reject_contract(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
    contract_id = int(request.POST.get('contractid'))
    contract = get_object_or_404(InternalContract, team=team, id=contract_id)
    
    if request.POST.get('action') == 'accept':
        InternalContract.capture(contract.id, contract.ACCEPTED)
        response = JsonResponse({'status': 'accepted'})
        return response

    elif request.POST.get('action') == 'reject':
        InternalContract.capture(contract.id, contract.REJECTED)
        response = JsonResponse({'status': 'rejected'})
        return response


@login_required
@user_is_client
def internal_contract_fee_structure(request, contract_id, contract_slug):
    base_contract = BaseContract(request)
    payment_gateways = PaymentGateway.objects.filter(status=True).exclude(name='Balance')
    contract = get_object_or_404(InternalContract, pk=contract_id, slug=contract_slug, reaction=InternalContract.ACCEPTED, created_by=request.user)
    discount = base_contract.get_discount_value(contract)
    multiplier = base_contract.get_discount_multiplier(contract)
    start_discount = base_contract.get_start_discount_value()

    context = {
        "contract": contract,
        "payment_gateways": payment_gateways,
        "discount": discount,
        "multiplier": multiplier,
        "start_discount": start_discount,
    }
    return render(request, 'contract/payment_fee_structure.html', context)


@login_required
@user_is_client
def contract_fee_selection(request):
    chosen_contract = BaseContract(request)
    session = request.session
    if request.POST.get('action') == 'capture-contract':
        contract_id = int(request.POST.get('contractid'))
        gateway_type = int(request.POST.get('gatewaytype'))
        contract = get_object_or_404(InternalContract, pk=contract_id, reaction=InternalContract.ACCEPTED, created_by=request.user)

        chosen_contract.capture(contract=contract)

        if "contractchosen" not in request.session:
            session["contractchosen"] = {"contract_id": contract.id}
            session.modified = True

        discount = chosen_contract.get_discount_value(contract)
        
        gateway = PaymentGateway.objects.get(id=gateway_type)

        if "contractgateway" not in request.session:
            session["contractgateway"] = {"gateway_id": gateway.id}
            session.modified = True
        else:
            session["contractgateway"]["gateway_id"] = gateway.id
            session.modified = True

        context = {
            'contract_fee': gateway.processing_fee,
            'discount': discount
        }

        response = JsonResponse(context)
        return response


@login_required
@user_is_client
def final_contract_checkout(request, contract_id, contract_slug):
    chosen_contract = BaseContract(request)
    contract = get_object_or_404(InternalContract, pk=contract_id, slug=contract_slug, reaction=InternalContract.ACCEPTED, created_by=request.user)

    if "contractchosen" not in request.session:
        messages.error(request, "Bad request. We could not fetch the selected contract. Try again")
        return redirect("contract:internal_contract_fee_structure", contract_id=contract.id, contract_slug=contract.slug)

    if "contractgateway" not in request.session:
        messages.error(request, "Please select payment option to proceed")
        return redirect("contract:internal_contract_fee_structure", contract_id=contract.id, contract_slug=contract.slug)

    clientsecret = ''
    context = {}
    discount = chosen_contract.get_discount_value(contract)
    multiplier = chosen_contract.get_discount_multiplier(contract)
    start_discount = chosen_contract.get_start_discount_value()
    selected_fee = chosen_contract.get_fee_payable()
    gateway_type = chosen_contract.get_gateway()
    subtotal = chosen_contract.get_total_price_before_fee_and_discount(contract)
    grand_total = chosen_contract.get_total_price_after_discount_and_fee(contract)
    

    # Stripe payment api
    stripe_public_key = StripeClientConfig().stripe_public_key()
    # Paypal payment api
    paypal_public_key = PayPalClientConfig().paypal_public_key()
    # Futterwave payment api
    flutterwave_public_key = FlutterwaveClientConfig().flutterwave_public_key()
    # Razorpay payment api
    razorpay_public_key = RazorpayClientConfig().razorpay_public_key_id()

    currency = CurrencyForm()
    base_currency = get_base_currency_code()

    context = {
        'contract': contract,
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
        "discount": discount,
        "multiplier": multiplier,
        "start_discount": start_discount,
        "paypal_public_key": paypal_public_key,
        "clientsecret": clientsecret,        
    }

    return render(request, "contract/final_contract_checkout.html", context)


@login_required
@user_is_client
def flutter_payment_intent(request):
    contract_id = request.session["contractchosen"]["contract_id"]

    chosen_contract = BaseContract(request)
    gateway_type = str(chosen_contract.get_gateway())

    contract = get_object_or_404(InternalContract, pk=contract_id, team_reaction=True, status=InternalContract.PENDING, created_by=request.user)
    
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)  
    grand_total = chosen_contract.get_total_price_after_discount_and_fee(contract)

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
            category = Purchase.CONTRACT,
            salary_paid=grand_total,
            unique_reference=unique_reference,           
        )           
        purchase.status=Purchase.FAILED
        purchase.save()

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


@login_required
def stripe_contract_intent(request):
    contract_id = request.session["contractchosen"]["contract_id"]
    chosen_contract = BaseContract(request)
    gateway_type = str(chosen_contract.get_gateway())
    contract = get_object_or_404(InternalContract, pk=contract_id, team_reaction=True, status=InternalContract.PENDING, created_by=request.user)
    
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)  
    grand_total = chosen_contract.get_total_price_after_discount_and_fee(contract)  

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
        success_url='http://' + str(get_current_site(request)) + '/contract/congrats/',
        cancel_url='http://' + str(get_current_site(request)) + '/dashboard/'
    )

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
            client_fee = int(total_gateway_fee),
            category = Purchase.CONTRACT,
            salary_paid=grand_total,
            unique_reference=stripe_reference,           
        )           
        purchase.stripe_order_key=payment_intent
        purchase.status=Purchase.FAILED
        purchase.save()

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

        chosen_contract.clean_box()
        return JsonResponse({'session': session,})
            
    return JsonResponse({'Perfect':'All was not successful',})


@login_required
def paypal_contract_intent(request):
    contract_id = request.session["contractchosen"]["contract_id"]
    chosen_contract = BaseContract(request)
    contract = get_object_or_404(InternalContract, pk=contract_id, team_reaction=True, status=InternalContract.PENDING, created_by=request.user)
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    gateway_type = chosen_contract.get_gateway()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)
 
    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)
    data = body["orderID"]

    if data:
        paypal_request_order = OrdersGetRequest(data)
        response = PayPalClient.paypal_httpclient().execute(paypal_request_order)

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
            status = Purchase.SUCCESS
        )

        contract.status=InternalContract.PAID
        contract.save()

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
    gateway_type = str(chosen_contract.get_gateway())
    total_gateway_fee = chosen_contract.get_fee_payable()
    contract = get_object_or_404(InternalContract, pk=contract_id, team_reaction=True, status=InternalContract.PENDING, created_by=request.user)   
    
    grand_total = chosen_contract.get_total_price_after_discount_and_fee(contract)
    gateway_type = chosen_contract.get_gateway()
    base_currency_code = get_base_currency_code()
    discount_value = chosen_contract.get_discount_value(contract)
    total_gateway_fee = chosen_contract.get_fee_payable()
    grand_total_before_expense = chosen_contract.get_total_price_before_fee_and_discount(contract)       
    
    razorpay_api = RazorpayClientConfig()
    unique_reference = razorpay_api.razorpay_unique_reference()

    purchase = Purchase.objects.create(
        client=request.user,
        full_name=f'{request.user.first_name} {request.user.last_name}',
        payment_method=str(gateway_type),
        category = Purchase.CONTRACT,
        client_fee = int(total_gateway_fee),
        salary_paid=grand_total,
        unique_reference=unique_reference,
    )
    purchase.status = Purchase.FAILED
    purchase.save()

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

    notes = {'Total Price': 'The total amount may change with discount'}
    currency = base_currency_code
    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_order = razorpay_client.order.create(dict(
        amount = int(grand_total * 100), 
        currency = currency, 
        notes = notes, 
        receipt = purchase.unique_reference
    ))
    print('razorpay_order', razorpay_order['id'])
    purchase.razorpay_order_key = razorpay_order['id']
    purchase.save()

    response = JsonResponse({'contract':contract.id, 'currency':currency, 'amount': (purchase.salary_paid), 'razorpay_order_key': purchase.razorpay_order_key})
    return response


@login_required
@user_is_client
def razorpay_webhook(request):
    chosen_contract = BaseContract(request)
    # contract_id = ''
    if request.POST.get('action') == 'razorpay-contract':   
        contract_id = int(request.POST.get('contractid'))
        razorpay_order_key = str(request.POST.get('orderid'))
        razorpay_payment_id = str(request.POST.get('paymentid'))
        razorpay_signature = str(request.POST.get('signature'))

        # print('contract_id:', contract_id)
        # print('razorpay_order_id:', razorpay_order_key)
        # print('razorpay_payment_id:',razorpay_payment_id)
        # print('razorpay_signature:',razorpay_signature)
        data ={
            'razorpay_order_id': razorpay_order_key,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }    
                 
        contract = get_object_or_404(InternalContract, pk=contract_id, team_reaction=True, status=InternalContract.PENDING, created_by=request.user)
        razorpay_client = RazorpayClientConfig().get_razorpay_client()
        purchase = Purchase.objects.get(razorpay_order_key=razorpay_order_key)

        purchase.razorpay_payment_id = razorpay_payment_id
        purchase.razorpay_signature = razorpay_signature
        purchase.save()

        signature = razorpay_client.utility.verify_payment_signature(data)
        if signature == True: #must return True for below code to run
            contract.status=InternalContract.PAID
            contract.save()

            purchase.status = Purchase.SUCCESS
            purchase.save()

            chosen_contract.clean_box()
            return JsonResponse({'Perfect':'All was successful',})

        else:
            purchase.status = Purchase.FAILED
            purchase.save()
            return JsonResponse({'failed':'Transaction failed, Razorpay will refund your money if you are already debited',})
                       

@login_required
@user_is_client
def contract_success(request):

    context = {
        "good": "All good"
    }
    return render(request, "contract/payment_success.html", context)


@login_required
def payment_success(request):
    chosen_contract = BaseContract(request)
    chosen_contract.clean_box()

    context = {
        "good": "good"
    }
    return render(request, "applications/payment_success.html", context)

# <...........................................................Contractor Section starts..........................................................>


@user_is_freelancer
def add_contractor(request):
    team = get_object_or_404(
        Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    contract_offerror = Contractor.objects.filter(team=team)

    if request.method == 'POST':
        contractorform = ContractorForm(request.POST)
        if contractorform.is_valid():
            contractor = contractorform.save(commit=False)
            contractor.created_by = request.user
            contractor.team = team
            contractor.save()

            messages.success(request, 'The contractor was added successfully!')
            return redirect('contract:contract_client')

    else:
        contractorform = ContractorForm()
    context = {
        'contractorform': contractorform,
        'team': team,
        'contract_offerror': contract_offerror,
    }
    return render(request, 'contract/add_contractor.html', context)


@login_required
@user_is_freelancer
def update_contractor(request, contractor_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[
                             request.user], status=Team.ACTIVE)
    contractor = get_object_or_404(Contractor, team=team, pk=contractor_id)

    if request.method == 'POST':
        update_contractor = ChangeContractorForm(
            request.POST, instance=contractor)

        if update_contractor.is_valid():
            update_contractor.save()

            messages.success(request, 'The contractor was modified!')
            return redirect('contract:contract_client')

    else:
        update_contractor = ChangeContractorForm(instance=contractor)

    context = {
        "update_contractor": update_contractor,
        "contractor": contractor,
    }
    return render(request, 'contract/modify_contractor.html', context)


@login_required
@user_is_freelancer
def delete_contractor(request, contractor_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[
                             request.user], status=Team.ACTIVE)
    contractor = get_object_or_404(Contractor, team=team, pk=contractor_id)
    contractor.delete()

    messages.success(request, f'The contractor was deleted!')
    return redirect('contract:contract_client')


# <...........................................................External Contract Section..........................................................>
@login_required
@user_is_freelancer
def create_external_contract(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[
                             request.user], status=Team.ACTIVE)

    if request.method == 'POST':
        contractform = ExternalContractForm(team, request.POST)
        contractorform = ContractorForm(request.POST)

        if contractform.is_valid():
            contract = contractform.save(commit=False)
            contract.created_by = request.user
            contract.team = team
            contract.slug = slugify(contract.client.name)
            contract.save()

            messages.success(request, 'The contract was added!')
            return redirect('contract:external_contract_list')

        if contractorform.is_valid():
            contractor = contractorform.save(commit=False)
            contractor.created_by = request.user
            contractor.team = team
            contractor.save()

            messages.success(
                request, f'The contractor "{contractor.name}" was added!')
            return redirect('contract:create_external_contract')

    else:
        contractform = ExternalContractForm(team)
        contractorform = ContractorForm()
    context = {
        'contractform': contractform,
        'contractorform': ContractorForm,
        'team': team,
    }
    return render(request, 'contract/add_external_contract.html', context)


@login_required
def external_contract_list(request):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[
                                 request.user], status=Team.ACTIVE)
        contracts = team.contractsteam.all()

    elif request.user.user_type == Customer.CLIENT:
        contracts = Contract.objects.filter(client__email=request.user.email)

    context = {
        "contracts": contracts,
    }
    return render(request, 'contract/external_contract_list.html', context)


@login_required
def external_contract_detail(request, contract_id, urlcode):
    if request.user.user_type == Customer.FREELANCER:
        contract = get_object_or_404(
            Contract, team__pk=request.user.freelancer.active_team_id, pk=contract_id, urlcode=urlcode)

    elif request.user.user_type == Customer.CLIENT:
        contract = get_object_or_404(
            Contract, pk=contract_id, urlcode=urlcode, client__email=request.user.email)

    context = {
        "contract": contract,
    }
    return render(request, 'contract/external_contract_detail.html', context)


@login_required
@user_is_client
def redeem_external_contract(request, urlcode, contract_slug):
    if request.user.user_type == Customer.CLIENT:
        payments = PaymentGateway.objects.filter(status=True)
        contract = get_object_or_404(
            Contract, urlcode=urlcode, slug=contract_slug, client__email=request.user.email)

    context = {
        "contract": contract,
        "payments": payments,
    }
    return render(request, 'contract/redeem_external_contract.html', context)


@login_required
# same contract can be applied many times so add contract ID to params --TODO
def contract_chat(request, contract_id, contract_slug):
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[
                                 request.user], status=Team.ACTIVE)
        contract = get_object_or_404(
            InternalContract, pk=contract_id, slug=contract_slug, team=team)

    elif request.user.user_type == Customer.CLIENT:
        contract = get_object_or_404(
            InternalContract, pk=contract_id, slug=contract_slug, created_by=request.user)

    content = request.POST.get('content', '')

    if content:
        ContractChat.objects.create(content=content, contract=contract,
                                    team=contract.proposal.team, sender=request.user)  # team__proposal=team,

    chats = ContractChat.objects.all()
    return render(request, 'contract/contract_chat.html', {'chats': chats, 'contract': contract})


@login_required
def contract_chatroom(request,  contract_id):
    contract = get_object_or_404(InternalContract, pk=contract_id)
    chats = contract.contractclientchat.all()
    if request.htmx:
        return render(request, 'contract/components/partial_contract_message.html', {'chats': chats})
    else:
        return render(request, 'contract/contract_chat.html', {'chats': chats})

