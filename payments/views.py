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
from .checkout_card import CreditCard
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages
from transactions.utilities import get_base_currency



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
def subscribe_with_balance(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
    
    if  "teamplan" not in request.session:
        messages.error(request, "Please select payment option")
        return redirect("teams:packages")
    
    try:
        package = Package.objects.get(type='team')
        Subscription.subscribe_with_balance(
            merchant=request.merchant, 
            team=team, 
            package=package
        )
        del request.session["teamplan"]["gateway_id"]
        request.session.modified = True
        messages.info(request, f'Action Successful')
        return HttpResponseClientRedirect('/team/packages/')
    except Exception as e:
        messages.error(request, f'Error! {e}')
        return HttpResponseClientRedirect('/team/packages/')
        # return HttpResponseClientRedirect('/team/subscription/')


@login_required
def paypal_package_order(request):
    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)

    data = body["orderID"]
    paypal_request_order = OrdersGetRequest(data)
    response = PayPalClient.client.execute(paypal_request_order)
    Subscription.objects.create(
        team=team,
        subscriber=request.user,
        price=response.result.purchase_units[0].plan.amount.value,

        payment_method='PayPal',
        status=True
    )
    return JsonResponse({'done':'done deal'})



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

