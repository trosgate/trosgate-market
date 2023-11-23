from django.shortcuts import render,get_object_or_404, redirect
from account.models import Customer
from freelancer.models import Freelancer, FreelancerAccount, FreelancerAction
from django.contrib.auth.decorators import login_required
from account.permission import user_is_freelancer
from teams.forms import TeamCreationForm
from teams.models import Team, Package
from .models import PaymentAccount, PaymentRequest, Subscription
from .forms import CreditCardForm, PaymentAccountForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import PaymentGateway
from general_settings.currency import get_base_currency_symbol
from .checkout.stripe import StripeClientConfig
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages
from transactions.utilities import get_base_currency
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import json



@login_required
@user_is_freelancer
def payment_vault(request):
    account = None
    gateways = PaymentGateway.objects.filter(status=True).exclude(name='Balance')
    if PaymentAccount.objects.filter(user=request.user).exists():
        account = get_object_or_404(PaymentAccount, user=request.user)
    else:
        account = PaymentAccount(user=request.user).save()
    
    if request.method == "POST":
        paymentForm = PaymentAccountForm(request.POST or None, instance=account)
        if paymentForm.is_valid():
            account_vault = paymentForm.save(commit=False)
            account_vault.user = request.user
            account_vault.save()

            return redirect("payments:payment_vault") 
    else:
        paymentForm = PaymentAccountForm(instance=account)
    context = {
        'paymentForm': paymentForm,
        'account': account,
        'base_currency': get_base_currency_symbol(),
        'gateways': gateways
    }
    return render(request, "payments/payment_details.html", context)


@login_required
@user_is_freelancer
def transfer_transactions(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    manager = FreelancerAction.objects.filter(team=team, manager=request.user, action_choice=FreelancerAction.TRANSFER)
    staff = FreelancerAction.objects.filter(team=team, team_staff=request.user, action_choice=FreelancerAction.TRANSFER)

    manager_transfers = ''
    staff_transfers = ''

    if manager:
        page = request.GET.get('page', 1)
        paginator = Paginator(manager, 10)
        try:
            manager_transfers = paginator.page(page)
        except PageNotAnInteger:
            manager_transfers = paginator.page(1)
        except EmptyPage:
            manager_transfers = paginator.page(paginator.num_pages)

    if staff:
        page = request.GET.get('page', 1)
        paginator = Paginator(staff, 10)

        try:
            staff_transfers = paginator.page(page)
        except PageNotAnInteger:
            staff_transfers = paginator.page(1)
        except EmptyPage:
            staff_transfers = paginator.page(paginator.num_pages)

    context = {
        'manager_transfers': manager_transfers,
        'staff_transfers': staff_transfers,
    }
    return render(request, "payments/transfer_transactions.html", context)


@login_required
@user_is_freelancer
def withdrawal_transactions(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    team_withdrawals = PaymentRequest.objects.filter(team=team, user=request.user)

    context = {
        'team_withdrawals': team_withdrawals,
    }
    return render(request, "payments/withdrawal_transactions.html", context)


@login_required
@never_cache
def subscribe_with_balance(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
    
    try:
        Subscription.subscribe_with_balance(
            merchant=request.merchant, 
            team=team, 
        )

        messages.info(request, f'Action Successful')
        return HttpResponseClientRedirect('/team/packages/')
    except Exception as e:
        messages.error(request, f'Error! {e}')
        return HttpResponseClientRedirect('/team/packages/')


@login_required
@never_cache
@require_http_methods(['POST'])
def subscribe_with_stripe(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
    
    card_token = request.POST.get('card_token')
    stripe_client = StripeClientConfig()
    try:
        subscription_id, client_secret = stripe_client.subscribe_customer(
            customer = request.user.email, 
            card_token = card_token,
            team = team
        )

        response_data = {
            'client_secret': client_secret,
            'payment_intent': subscription_id
        }

        return JsonResponse(response_data)
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'status': 'failed'})


@login_required
@never_cache
@require_http_methods(['POST'])
def stripe_confirmation(request):
    subscription_id = request.POST.get('subscription_id', '')
    try:
        StripeClientConfig().confirm_subscription(subscription_id)
        transaction_url = reverse('teams:packages') 
        return JsonResponse({'status': 'success', 'transaction_url':transaction_url})
    except Exception as e:
        print('%s' % (str(e)))
        return JsonResponse({'status': 'failed'})


@login_required
@never_cache
@require_http_methods(['GET'])
def paypal_subscription(request):
    body = json.loads(request.body)
    paypal_order_key = body["paypal_order_key"]
    print(paypal_order_key)

    return JsonResponse({'error': 'Invalid request method'})
    # paypal_order_key = PayPalClientConfig().create_order(grand_total)
    # if paypal_order_key:
    #     try:
    #         purchase = Purchase.create_purchase_and_sales(
    #             client=request.user,
    #             **payment_data,
    #             category=Purchase.PROPOSAL,
    #             paypal_order_key=paypal_order_key,
    #             hiringbox=hiringbox,
    #         )
    #         response_data = {
    #             'paypal_order_key': paypal_order_key,
    #         }
    #         print('purchase ID ::', purchase.id)
    #         return JsonResponse(response_data)
    #     except Exception as e:
    #         print('purchase ID ::', str(e))
    #         return JsonResponse({'error': 'Invalid request method'})
    # else:
    #     print('purchase ID ::', str(e))
    #     return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
@never_cache
@require_http_methods(['POST'])
def paypal_callback(request):
    body = json.loads(request.body)
    paypal_order_key = body["paypal_order_key"]

    capture_data = PayPalClientConfig().capture_order(paypal_order_key)
    capture_data_id = capture_data['purchase_units'][0]['payments']['captures'][0]['id']
    if capture_data['status'] == 'COMPLETED':
        Purchase.paypal_order_confirmation(paypal_order_key, capture_data_id)
        hiringbox.clean_box()
        return JsonResponse(capture_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@login_required
def package_transaction(request):
    base_currency = get_base_currency(request)
    team = None
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)    
        subscriptions = Subscription.objects.filter(team=team)
        print(subscriptions)
    elif request.user.user_type == Customer.MERCHANT:
        subscriptions = Subscription.objects.filter(merchant=request.merchant)

    context = {
        'subscriptions':subscriptions,
        'base_currency': base_currency,       
    }
    return render(request, 'payments/package_transactions.html', context)


