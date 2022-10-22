from django.shortcuts import render,get_object_or_404
from account.models import Customer
from freelancer.models import Freelancer, FreelancerAccount, FreelancerAction
from django.contrib.auth.decorators import login_required
from account.permission import user_is_freelancer
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from .models import PaymentAccount, PaymentRequest
from .forms import PaymentAccountForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from general_settings.models import PaymentGateway


@login_required
@user_is_freelancer
def payment_vault(request):
    account = None
    gateways = PaymentGateway.objects.filter(status=True)

    if PaymentAccount.objects.filter(user=request.user).exists():
        account = get_object_or_404(PaymentAccount, user=request.user)
        paymentForm = PaymentAccountForm(instance=account)
    else:
        account = PaymentAccount(user=request.user).save()
        paymentForm = PaymentAccountForm(instance=account)
       
    context = {
        'paymentForm': paymentForm,
        'account': account,
        'gateways': gateways
    }
    return render(request, "payments/payment_details.html", context)


@login_required
@user_is_freelancer
def update_payment_account(request):
    user = get_object_or_404(PaymentAccount, user=request.user, user__is_active=True, user__user_type=Customer.FREELANCER)
    message = ''
    mes = ''
    if request.POST.get('action') == 'payment-account':
        paypal = str(request.POST.get('paypalAccount', ''))
        stripe = str(request.POST.get('stripeAccount', ''))
        flutterwave = str(request.POST.get('flutterwaveAccount', ''))
        razorpay = str(request.POST.get('razorpayAccount', ''))

        print(paypal, stripe, flutterwave, razorpay)

        try:
            PaymentAccount.payment_mode(
                user=user,
                paypal=paypal,
                stripe=stripe,
                flutterwave=flutterwave,
                razorpay=razorpay,
            )

            message = f'The account was updated successfully'
        except Exception as e:
            mes = str(e)
            message = message = f'<span id="debit-message" class="alert alert-danger" style="color:red; text-align:right;">{mes}</span>'

        return JsonResponse({'message': message})


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


