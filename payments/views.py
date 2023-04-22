from django.shortcuts import render,get_object_or_404, redirect
from account.models import Customer
from freelancer.models import Freelancer, FreelancerAccount, FreelancerAction
from django.contrib.auth.decorators import login_required
from account.permission import user_is_freelancer
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from .models import PaymentAccount, PaymentRequest
from .forms import CreditCardForm, PaymentAccountForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import PaymentGateway
from general_settings.currency import get_base_currency_symbol
from .checkout_card import CreditCard



# def paypal(request):
#     amount = 1
#     response = None
#     if request.method == 'POST':
#         form = CheckoutCardForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             credit_card = CreditCard(**data)
#             merchant = get_gateway("pay_pal")
#             try:
#                 merchant.validate_card(credit_card)
#             except CardNotSupported:
#                 response = "Credit Card Not Supported"
#             # response = merchant.purchase(amount, credit_card, options={'request': request})
#             response = merchant.recurring(amount, credit_card, options={'request': request})
#     else:
#         form = CreditCardForm(initial=GATEWAY_INITIAL['paypal'])
#     return render(request, 'app/index.html', {'form': form,
#                                               'amount': amount,
#                                               'response': response,
#                                               'title': 'Paypal'})


# def stripe(request):
#     amount = 1
#     response= None
#     if request.method == 'POST':
#         form = CheckoutCardForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             credit_card = CreditCard(**data)
#             merchant = get_gateway("stripe")
#             response = merchant.purchase(amount,credit_card)
#     else:
#         form = CreditCardForm(initial=GATEWAY_INITIAL['stripe'])
#     return render(request, 'app/index.html',{'form': form,
#                                              'amount':amount,
#                                              'response':response,
#                                              'title':'Stripe Payment'})



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


