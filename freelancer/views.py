from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from . forms import FreelancerForm, FundTransferForm, WithdrawalForm
from django.contrib.auth import login
from account.models import Customer
from . models import Freelancer, FreelancerAccount, FreelancerAction
from proposals.models import Proposal
from projects.models import Project
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from account.permission import user_is_freelancer
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from teams.controller import max_member_per_team
from contract.forms import InternalContractForm
from django.db.models import F
from teams.controller import monthly_offer_contracts
from django.db import transaction
from account.fund_exception import FundException
import json
from general_settings.fund_control import get_min_balance, get_min_transfer, get_max_transfer, get_min_withdrawal, get_max_withdrawal
from general_settings.currency import get_base_currency_symbol
from future.utilities import get_transfer_feature



@login_required
def freelancer_profile(request, short_name):
    freelancer = get_object_or_404(Freelancer, user__short_name=short_name)
    team = get_object_or_404(Team, pk=freelancer.active_team_id, status=Team.ACTIVE)
    monthly_contracts_limiter = monthly_offer_contracts(team)
    print(team)
    print(monthly_contracts_limiter)
    context = {
        'freelancer': freelancer,
        'team': team,
        'monthly_contracts_limiter': monthly_contracts_limiter,
    }
    return render(request, 'freelancer/freelancer_profile_detail.html', context)


@login_required
def update_freelancer(request, user_id):
    freelancer = get_object_or_404(Freelancer, user_id=user_id, user=request.user)
    if request.method == 'POST':
        profileform = FreelancerForm(request.POST, request.FILES, instance=freelancer)

        if profileform.is_valid():
            freelancer = profileform.save(commit=False)
            freelancer.user = request.user

            freelancer.save()
            profileform.save_m2m()  # for saving manytomany items in forms

            messages.info(request, 'Profile updated Successfully')

            return redirect("account:dashboard")

    else:
        profileform = FreelancerForm(instance=freelancer)

    context = {
        'profileform': profileform,
        'freelancer': freelancer,
    }
    return render(request, 'freelancer/freelancer_profile_update.html', context)


def freelancer_listing(request):
    freelancer_profile_list = Freelancer.objects.filter(user__is_active=True, user__user_type=Customer.FREELANCER)
    context = {
        'freelancer_profile_list': freelancer_profile_list,
    }
    return render(request, 'freelancer/freelancer_listing.html', context)


@login_required
@user_is_freelancer
def transfer_or_withdraw(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    team_staff = request.user.team_member.filter(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)

    manager_transfers = FreelancerAction.objects.filter(team=team, manager=request.user)
    staff_transfers = FreelancerAction.objects.filter(team=team, team_staff=request.user)
    transferform = FundTransferForm(team_staff)
    withdrawalform = WithdrawalForm(request.POST)

    min_balance_remaining = get_min_balance()
    max_transfer_amount = get_max_transfer()
    min_transfer_amount = get_min_transfer()
    max_withdrawal_amount = get_max_withdrawal()
    min_withdrawal_amount = get_min_withdrawal()
    base_currency = get_base_currency_symbol()

    context = {
        'team': team,
        'transferform': transferform,
        'withdrawalform': withdrawalform,
        'manager_transfers': manager_transfers,
        'staff_transfers': staff_transfers,
        'min_balance_remaining': min_balance_remaining,
        'max_transfer_amount': max_transfer_amount,
        'min_transfer_amount': min_transfer_amount,
        'max_withdrawal_amount': max_withdrawal_amount,
        'min_withdrawal_amount': min_withdrawal_amount,
        'base_currency': base_currency,
    }
    return render(request, "freelancer/fund_transfer_withdraw.html", context)


@login_required
@user_is_freelancer
def transfer_debit(request):
    team = get_object_or_404(Team, created_by=request.user, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    message = ''
    mes = ''
    if request.POST.get('action') == 'make-transfer' and get_transfer_feature():
        team_staff_id = int(request.POST.get('teamstafftype'))
        position = str(request.POST.get('position'))
        debit_amount = int(request.POST.get('tamount'))
        staff = Customer.objects.get(id=team_staff_id)

        try:
            FreelancerAccount.transfer(
                team_owner=team.created_by, 
                team_staff=staff, 
                transfer_status=True,
                action_choice=FreelancerAction.TRANSFER, 
                team=team, 
                debit_amount=debit_amount, 
                position=position
            )
            mes = f'The amount ${debit_amount} was successfully transfered to {staff.get_full_name()}'
            message = f'<span id="debit-message" class="alert alert-info" style="color:green; text-align:right;">{mes}</span>'
        
        except FundException as e:
            mes = str(e)
            message = f'<span id="debit-message" class="alert alert-danger" style="color:red; text-align:right;">{mes}</span>'

        response = JsonResponse({'message': message})
        return response

    response = JsonResponse({'message': f'<span id="debit-message" class="alert alert-danger" style="color:red; text-align:right;">Bad request. Contact Support</span>'})
    return response


@login_required
@user_is_freelancer
def withdrawal_debit(request):
    team = get_object_or_404(Team, created_by=request.user, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    message = ''
    mes = ''
    if request.POST.get('action') == 'make-withdrawal':
        withdraw_amount = int(request.POST.get('wamount'))
        narration = str(request.POST.get('narration'))

        try:
            FreelancerAccount.withdrawal(
                team_owner=team.created_by,
                team_staff=team.created_by,
                action_choice=FreelancerAction.WITHDRAWAL,
                team=team,
                withdraw_amount=withdraw_amount,
                narration=narration,
                transfer_status=True
            )

            message = f'The withdrawal for ${withdraw_amount} was initiated'
        except FundException as e:
            mes = str(e)
            message = message = f'<span id="debit-message" class="alert alert-danger" style="color:red; text-align:right;">{mes}</span>'

        return JsonResponse({'message': message})
