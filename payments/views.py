from django.shortcuts import render,get_object_or_404
from freelancer.models import Freelancer, FreelancerAccount, FreelancerAction
from django.contrib.auth.decorators import login_required
from account.permission import user_is_freelancer
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from .models import PaymentRequest


@login_required
@user_is_freelancer
def transfer_transactions(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    manager_transfers = FreelancerAction.objects.filter(team=team, manager=request.user, action_choice=FreelancerAction.TRANSFER)
    staff_transfers = FreelancerAction.objects.filter(team=team, team_staff=request.user, action_choice=FreelancerAction.TRANSFER)

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


