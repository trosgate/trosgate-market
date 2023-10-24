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
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from teams.controller import max_member_per_team
from django.db.models import F
from account.fund_exception import FundException
import json
from general_settings.fund_control import get_min_balance, get_min_transfer, get_max_transfer, get_min_withdrawal, get_max_withdrawal
from future.utilities import get_transfer_feature
from account.models import Country
from general_settings.models import Category, Skill
from payments.models import PaymentGateway
from teams.models import Team
from account.models import Customer
from proposals.models import Proposal
from django.template.loader import render_to_string
from .utilities import (
    one_month, two_months, three_months, four_months, five_months, six_months,
    one_year, two_years, three_years, four_years, five_years    
)
from django.core.paginator import Paginator
from analytics.analytic import (
    ongoing_founder_projects, completed_founder_projects,
    cancelled_founder_projects, total_verified_sale,
    user_review_rate, total_projects_in_queue
)
from transactions.utilities import get_base_currency



# this will appear in search results
def freelancer_listing(request):
    freelancer_list = Freelancer.objects.filter(created=True)
    categorie = Category.objects.filter(visible = True).distinct()
    countries = Country.objects.filter(supported = True).distinct()
    skills = Skill.objects.all().distinct()
    base_currency = get_base_currency(request)
    all_freelancers = freelancer_list.count()

    totalcount = f' There are {all_freelancers} Freelancers available for search'
    context = {
        "freelancer_list": freelancer_list,
        "skills":skills, 
        "countries":countries, 
        "categorie":categorie, 
        "base_currency": base_currency,
        "totalcount": totalcount        
    }
    return render(request, 'freelancer/freelancer_listing.html', context)


def freelancer_search(request):
    freelancer_list = Freelancer.objects.filter(created=True)
    base_currency = get_base_currency(request)
    #Country
    country = request.GET.getlist('country[]')
    # Skills
    skill = request.GET.getlist('skill[]')
    # Upgraded Teams
    upgraded_founder = request.GET.get('upgradedfreelancer[]', '')
    basic_founder = request.GET.get('basicfreelancer[]', '')
    # User Joined Date
    join_one_month = request.GET.get('join_one_month[]', '')
    join_two_month = request.GET.get('join_two_month[]', '')
    join_three_month = request.GET.get('join_three_month[]', '')
    join_four_month = request.GET.get('join_four_month[]', '')
    join_five_month = request.GET.get('join_five_month[]', '')
    join_six_month = request.GET.get('join_six_month[]', '')
    join_one_year = request.GET.get('join_one_year[]', '')
    join_two_year = request.GET.get('join_two_year[]', '')
    join_three_year = request.GET.get('join_three_year[]', '')
    join_four_year = request.GET.get('join_four_year[]', '')
    join_over_five_year = request.GET.get('join_over_five_year[]', '')

    all_freelancers = freelancer_list.count()

    # Country
    if len(country) > 0:
        freelancer_list = freelancer_list.filter(user__country__id__in=country).distinct()
    # Skills    
    if len(skill) > 0:
        freelancer_list = freelancer_list.filter(skill__id__in=skill).distinct()

    # Upgraded Teams
    if upgraded_founder != '':
        teams = Team.objects.filter(status=Team.ACTIVE, package_status=Team.ACTIVE).values_list('created_by').distinct()
        freelancer_list = freelancer_list.filter(user__in=list(teams))

    # Basic Teams
    if basic_founder != '':
        teams = Team.objects.filter(status=Team.ACTIVE, package_status=Team.DEFAULT).values_list('created_by').distinct()
        freelancer_list = freelancer_list.filter(user__in=list(teams))

    # User Joined Date
    if join_one_month != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=one_month()).distinct()
    if join_two_month != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=two_months()).distinct()
    if join_three_month != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=three_months()).distinct()
    if join_four_month != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=four_months()).distinct()
    if join_five_month != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=five_months()).distinct()
    if join_six_month != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=six_months()).distinct()
    if join_one_year != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=one_year()).distinct()
    if join_two_year != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=two_years()).distinct()
    if join_three_year != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=three_years()).distinct()
    if join_four_year != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=four_years()).distinct()
    if join_over_five_year != '':
        freelancer_list = freelancer_list.filter(user__date_joined__lte=five_years()).distinct()

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
    team = get_object_or_404(Team, pk=freelancer.active_team_id)
    monthly_contract_slot = team.monthly_contract_slot
    ongoing_projects = ongoing_founder_projects(team)
    completed_projects = completed_founder_projects(team)
    cancelled_projects = cancelled_founder_projects(team)
    verified_sale = total_verified_sale(team)
    review_rate = user_review_rate(team)
    projects_in_queue = total_projects_in_queue(team)

    context = {
        'freelancer': freelancer,
        'team': team,
        'monthly_contract_slot': monthly_contract_slot,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
        'cancelled_projects': cancelled_projects,
        'verified_sale': verified_sale,
        'good_review_rate': review_rate,
        'projects_in_queue': projects_in_queue
        
    }
    return render(request, 'freelancer/freelancer_profile_detail.html', context)


@login_required
@user_is_freelancer
def update_freelancer(request, short_name):
    freelancer = get_object_or_404(Freelancer, user__short_name=short_name, user=request.user)
    if request.method == 'POST':
        profileform = FreelancerForm(request.POST, request.FILES, instance=freelancer)

        if profileform.is_valid():
            freelancer = profileform.save(commit=False)
            freelancer.user = request.user
            freelancer.merchant = request.merchant
            freelancer.created = True

            freelancer.save()
            profileform.save_m2m()  # for saving manytomany items in forms

            messages.info(request, 'Profile updated Successfully')

            return redirect("freelancer:update_freelancer_profile", short_name=freelancer.user.short_name)

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
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, created_by=request.user)
    team_staff = request.user.team_member.filter(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)

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
        position = str(request.POST.get('position', ''))
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
            message = f'<span id="debit-message" style="color:green; text-align:right;">{mes}</span>'
        
        except FundException as e:
            mes = str(e)
            message = f'<span id="debit-message" style="color:red; text-align:right;">{mes}</span>'

        response = JsonResponse({'message': message})
        return response

    response = JsonResponse({'message': f'<span id="debit-message" style="color:red; text-align:right;">Bad request. Contact Support</span>'})
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
        gateway_id = int(request.POST.get('gateway'))

        try:
            gateway = PaymentGateway.objects.get(pk=gateway_id)
            FreelancerAccount.withdrawal(
                team_owner=team.created_by,
                team_staff=team.created_by,
                action_choice=FreelancerAction.WITHDRAWAL,
                team=team,
                gateway=gateway,
                withdraw_amount=withdraw_amount,
                narration=narration,
                transfer_status=True
            )

            message = f'The withdrawal for ${withdraw_amount} was initiated'
        except FundException as e:
            mes = str(e)
            message = message = f'<span id="debit-message" style="color:red; text-align:right;">{mes}</span>'

        return JsonResponse({'message': message})

