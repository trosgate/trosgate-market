from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from . forms import FreelancerForm, FundTransferForm, WithdrawalForm
from . models import Freelancer, FreelancerAccount, FreelancerAction
from django.http import JsonResponse
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
from account.fund_exception import FundException
import json
from general_settings.fund_control import get_min_balance, get_min_transfer, get_max_transfer, get_min_withdrawal, get_max_withdrawal
from future.utilities import get_transfer_feature
from account.models import Country
from general_settings.models import Category, Skill
from teams.models import Team
from account.models import Customer
from proposals.models import Proposal
from django.template.loader import render_to_string
from general_settings.currency import get_base_currency_symbol, get_base_currency_code

#this will appear in search results
def freelancer_listing(request):
    freelancer_list = Freelancer.active.all()
    categorie = Category.objects.filter(visible = True).distinct()
    countries = Country.objects.filter(supported = True).distinct()
    skills = Skill.objects.all().distinct()
    base_currency = get_base_currency_symbol()
    base_currency = get_base_currency_symbol()
    all_freelancers = freelancer_list.count()

    totalcount = f' There are {all_freelancers} Freelancers available for search'
    context = {
        'freelancer_list': freelancer_list,
        "skills":skills, 
        "countries":countries, 
        "categorie":categorie, 
        "base_currency": base_currency,
        "totalcount": totalcount,        
    }
    return render(request, 'freelancer/freelancer_listing.html', context)


def freelancer_search(request):
    freelancer_list = ''
    base_currency = get_base_currency_symbol()
    #Country
    country = request.GET.getlist('country[]')
    # Skills
    skill = request.GET.getlist('skill[]')
    # # Upgraded Teams
    upgraded_founder = request.GET.get('upgradedfreelancer[]', '')

    # # Duration
    # one_day = request.GET.get('one_day[]', '')
    # two_days = request.GET.get('two_days[]', '')
    # three_days = request.GET.get('three_days[]', '')
    # four_days = request.GET.get('four_days[]', '')
    # five_days = request.GET.get('five_days[]', '')
    # six_days = request.GET.get('six_days[]', '')
    # one_week = request.GET.get('one_week[]', '')
    # two_weeks = request.GET.get('two_weeks[]', '')
    # three_weeks = request.GET.get('three_weeks[]', '')
    # one_month = request.GET.get('one_month[]', '')
    # # Upgraded Teams
    # upgraded_teams = request.GET.get('upgradedTeams[]', '')

    freelancers = Freelancer.active.all()
    all_freelancers = freelancers.count()
    #Country
    if len(country) > 0:
        freelancer_list = freelancers.filter(user__country__id__in=country).distinct()

    # Skills    
    if len(skill) > 0:
        freelancer_list = freelancers.filter(skill__id__in=skill).distinct()

    # Upgraded Teams
    if upgraded_founder != '':
        teams = Team.objects.filter(status=Team.ACTIVE, package_status=Team.ACTIVE)
        for founder in teams:
            print('names:', founder.created_by.short_name)
            all_founders = founder.created_by.id
            print('all_founders:::', founder.title)

        freelancer_list = freelancers.filter(user__id__in=[all_founders])
        print('freelancer_list:::', freelancer_list)
    # if revision_false != '':
    #     proposals = proposals.filter(revision=False).distinct()
    # # Duration
    # if one_day != '':
    #     proposals = proposals.filter(dura_converter = one_day).distinct()
    # if two_days != '':
    #     proposals = proposals.filter(dura_converter = two_days).distinct()
    # if three_days != '':
    #     proposals = proposals.filter(dura_converter = three_days).distinct()
    # if four_days != '':
    #     proposals = proposals.filter(dura_converter = four_days).distinct()
    # if five_days != '':
    #     proposals = proposals.filter(dura_converter = five_days).distinct()
    # if six_days != '':
    #     proposals = proposals.filter(dura_converter = six_days).distinct()
    # if one_week != '':
    #     proposals = proposals.filter(dura_converter = one_week).distinct()
    # if two_weeks != '':
    #     proposals = proposals.filter(dura_converter = two_weeks).distinct()
    # if three_weeks != '':
    #     proposals = proposals.filter(dura_converter = three_weeks).distinct()
    # if one_month != '':
    #     proposals = proposals.filter(dura_converter = one_month).distinct()
    # # Upgraded Teams
    # if upgraded_teams != '':
    #     proposals = proposals.filter(team__package__type = 'Team').distinct()

    search_count = len(freelancer_list)
    totalcount = f'<div id="freelancerTotal" class="alert alert-info text-center" role="alert" style="color:black;">{search_count} of {all_freelancers} search results found</div>'

    searched_freelancer = render_to_string('freelancer/ajax/freelancer_search.html', {'freelancer_list':freelancer_list, 'base_currency':base_currency})
    if len(freelancer_list) > 0: 
        return JsonResponse({'freelancer_list': searched_freelancer, 'base_currency':base_currency, 'totalcount':totalcount})
    else:
        searched_freelancer = f'<div class="alert alert-warning text-center" role="alert" style="color:red;"> Hmm! nothing to show for this search</div>'
        return JsonResponse({'freelancer_list': searched_freelancer, 'base_currency':base_currency, 'totalcount':totalcount})


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
