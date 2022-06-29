import random
import json
import stripe
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Invitation, TeamChat, AssignMember, Tracking, Package
from django.contrib.auth.decorators import login_required
from .forms import TeamCreationForm, InvitationForm, TeamChatForm, AssignForm
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from account.models import Customer
from account.permission import user_is_freelancer
from django.http import HttpResponseRedirect
from .tasks import email_all_users
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .utilities import create_random_code, send_invitation_email, send_invitation_accepted_mail
from django.http import JsonResponse
from proposals.models import Proposal
from django.db.models import F, Q
from projects.models import Project
from applications.models import Application
from account.models import Customer
from datetime import datetime
from teams.controller import max_member_per_team
from django.views.decorators.http import require_http_methods
from freelancer.models import Freelancer
from general_settings.gateways import PayPalClientConfig, StripeClientConfig, FlutterwaveClientConfig, RazorpayClientConfig
from paypalcheckoutsdk.orders import OrdersGetRequest
from transactions.models import Purchase, SubscriptionItem
from general_settings.models import PaymentAPIs
from django.conf import settings
from . controller import monthly_projects_applicable_per_team
from account.fund_exception import InvitationException

def send_email_to_all_users(request):
    email_all_users.delay()
    return HttpResponse('Mail Sent')


# Instead of hard-coding tasks,
# I want Admin to have flexibility to schedule without coding skill required
def Admin_email_scheduler(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour=21, minute=20)
    task = PeriodicTask.objects.create(
        crontab=schedule, name='mail_schedule_' + create_random_code()[:5], task='teams.tasks.email_all_users')
    return HttpResponse('completed')


@login_required
@user_is_freelancer
def team(request):
    team = Team.objects.filter(status=Team.ACTIVE, pk=request.user.freelancer.active_team_id)
    # teams = team.teams.all()

    context = {
        # 'teamform': teamform,
        # 'teams': teams,
    }
    return render(request, 'teams/add_team.html', context)


@login_required
@user_is_freelancer
def activate_team(request, team_id):
    '''
    User can switch from current active team 
    User will activate an inactive team and operate in that team
    '''
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])

    freelancer = request.user.freelancer
    freelancer.active_team_id = team.id
    freelancer.save()

    messages.info(request, f'The team "{team.title}" was activated')

    return redirect('account:dashboard')


@login_required
def preview_team(request, team_id):
    teams = get_object_or_404(Team, pk=team_id, members__in=[request.user])

    return render(request, 'teams/preview_inactive_team.html', {"teams": teams})


@login_required
@user_is_freelancer
def update_teams(request, team_id):
    update_team = get_object_or_404(
        Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])

    if request.method == 'POST':
        update_teamform = TeamCreationForm(request.POST, instance=update_team)

        if update_teamform.is_valid():
            update_teamform.instance.slug = slugify(update_team.title)
            update_teamform.save()

            messages.success(request, 'The Changes were saved successfully!')

            return HttpResponseRedirect(reverse('account:dashboard'))

    else:
        update_teamform = TeamCreationForm(instance=update_team)
    context = {
        "update_teamform": update_teamform,
    }
    return render(request, 'teams/update_team.html', context)


@login_required
@user_is_freelancer
def team_single(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    proposals = team.proposalteam.all()
    proposal_assigned = team.assignteam.all()
    applications = team.applications.all()
    invited = Invitation.objects.filter(team=team, status=Invitation.INVITED)
    accepted = Invitation.objects.filter(team=team, status=Invitation.ACCEPTED)
    code = Invitation.objects.values('code')

    # to show invite
    context = {
        "teams": team,
        "code": code,
        'invited': invited,
        'accepted': accepted,
        "proposals": proposals,
        "applications": applications,
        "proposal_assigned": proposal_assigned,
    }
    return render(request, 'teams/team_detail.html', context)


@login_required
@user_is_freelancer
def delete_teams(request, team_id):
    delete_team = get_object_or_404(Team, pk=team_id, created_by=request.user, members__in=[request.user])
    delete_team.delete()
    messages.success(request, 'The Changes were saved successfully!')
    return redirect("teams:team")


# Inviting a user that already
@login_required
@user_is_freelancer
def invitation(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, created_by=request.user)
    invited = team.invitations.filter(status=Invitation.INVITED)
    accepted = team.invitations.filter(status=Invitation.ACCEPTED)
    code = Invitation.objects.values('code')[0]
    max_team_members = max_member_per_team(team)

    monthly_projects_applicable_per_team(request)

    inviteform = InvitationForm()

    context = {
        "teams": team,
        "inviteform": inviteform,
        "code": code,
        'invited': invited,
        'accepted': accepted,
        'max_team_members': max_team_members,
    }
    return render(request, 'teams/invitation_detail.html', context)


# remove team member
# Inviting a user that already exist to your team via user profile page
@login_required
@user_is_freelancer
def internal_invitation(request):
    result = ''
    errors = ''
    if request.POST.get("action") == "send-invite":
        pk = int(request.POST.get('freelancerId'))

        receiver = Customer.objects.get(pk=pk, is_active=True)       
        team = Team.objects.get(pk=request.user.freelancer.active_team_id, created_by=request.user)

        try:
            new_invite = Invitation.internal_invitation(
                team=team, 
                sender=request.user, 
                type=Invitation.INTERNAL, 
                receiver=receiver, 
                email=receiver.email
            )
            send_invitation_email(new_invite.email, new_invite.code, new_invite.team)
            result = 'The user was invited successfully'
        except InvitationException as e: 
            errors = str(e)

        return JsonResponse({'result':result, 'errors':errors})

@login_required
@user_is_freelancer
def external_invitation(request):
    result = ''
    errors = ''
    if request.POST.get("action") == "email-invite":
        email = str(request.POST.get('emailId'))

        team = Team.objects.get(pk=request.user.freelancer.active_team_id, created_by=request.user)

        try:
            new_invite = Invitation.external_invitation(
                team=team, 
                sender=request.user, 
                type=Invitation.EXTERNAL, 
                email=email
            )
            send_invitation_email(new_invite.email, new_invite.code, new_invite.team)
            result = 'The user was invited successfully'
        except InvitationException as e: 
            errors = str(e)

        return JsonResponse({'result':result, 'errors':errors})
        

# email-invite

# @login_required
# @user_is_freelancer
# def internal_invitation_old(request, short_name):
#     package = get_object_or_404(Package, pk=2, type='Team')
#     team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, package=package, status=Team.ACTIVE, created_by=request.user)
#     code = Invitation.objects.values('code')[0]

#     if team:
#         for invitee in Customer.objects.filter(short_name=short_name, is_active=True, user_type=Customer.FREELANCER):
#             try:
#                 if invitee:
#                     invitation = Invitation.objects.filter(
#                         team=team, email=invitee.email)

#                     if not invitation:

#                         member = Invitation.objects.create(
#                             team=team, email=invitee.email, status=Invitation.INVITED)

#                         email = member.email

#                         send_invitation_email(email, code, team)

#                         if member:
#                             return redirect('account:dashboard')
#                         else:
#                             messages.error(
#                                 request, 'Something went wrong. Please contact Admin')
#                     else:
#                         messages.info(
#                             request, f'The new member "{invitee.short_name}" was invited to {team.title}')
#             except:
#                 messages.error(
#                     request, 'Something went wrong. Please contact Admin')

#     return redirect('account:dashboard')


@login_required
@user_is_freelancer
def accept_team_invitation(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    if not team:
        return redirect('account:dashboard')

    if request.method == "POST":
        code = request.POST.get('code')
        if code:
            invitations = Invitation.objects.filter(code=code, email=request.user.email)

            if invitations:
                invitation = invitations[0]
                invitation.status = Invitation.ACCEPTED
                invitation.save()

                team = invitation.team
                team.members.add(request.user)
                team.save()

                freelancer = request.user.freelancer
                freelancer.active_team_id = team.id
                freelancer.save()

                messages.info(
                    request, f'Hi "{request.user.short_name}", you are now member of {team.title}')

                send_invitation_accepted_mail(team, invitation)

                return redirect('account:dashboard')
            else:
                messages.error(request, 'Sorry! No invitation for the given information')
        else:
            messages.error(
                request, f'Invalid code. Please contact team founder to assist')

    return render(request, 'teams/accept_team_invitation.html')


@login_required
@user_is_freelancer
def teamchat(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    content = request.POST.get('content', '')

    if content != '':
        TeamChat.objects.create(content=content, team=team, sender=request.user, is_sent=True)

    chats = team.teamchats.all()
    return render(request, 'teams/components/partial_team_message.html', {'chats': chats})


@login_required
@user_is_freelancer
def teamchatroom(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    chats = team.teamchats.all()
    admin = Customer.objects.filter(user_type=Customer.ADMIN, is_active=True, is_admin=True).first()
    if request.htmx:
        return render(request, 'teams/components/partial_team_message.html', {'chats': chats})
    else:
        return render(request, 'teams/active_team_chat.html', {'chats': chats, 'admin': admin, 'date_and_time': datetime.now().today()})


@login_required
@user_is_freelancer
def assign_proposal(request, team_slug, proposal_slug):
    team = get_object_or_404(Team, slug=team_slug, pk=request.user.freelancer.active_team_id,status=Team.ACTIVE, members__in=[request.user])
    proposal = get_object_or_404(Proposal, slug=proposal_slug, team=team)
    assignee = request.user.team_member.filter(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)

    if request.method == 'POST':

        assignform = AssignForm(assignee, request.POST)
        if assignform.is_valid():
            assign = assignform.save(commit=False)
            assign.team = team
            assign.proposal = proposal
            assign.assignor = request.user
            assign.is_assigned = True
            assign.save()

            messages.info(request, f'Member - "{assign.assignee.short_name}" assigned successfuly')

            return redirect('teams:team_single', team_id=team.id)

    else:
        assignform = AssignForm(assignee)

    context = {
        'assignform': assignform,
        'proposal': proposal,
        'team': team,
    }
    return render(request, 'teams/assign_member.html', context)


@login_required
@user_is_freelancer
def assign_proposals_to_me(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    assigned = team.assignteam.filter(assignee=request.user, is_assigned=True)

    context = {
        'team': team,
        'assigned': assigned,
    }
    return render(request, 'teams/assigned_task_to_me.html', context)


@login_required
@user_is_freelancer
def reassign_proposals_to_myself(request, member_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id,status=Team.ACTIVE, members__in=[request.user])
    if not (AssignMember.objects.filter(pk=member_id, team=team, assignee=request.user, is_assigned=True)).exists():
        AssignMember.objects.filter(pk=member_id, team=team, is_assigned=True).update(assignee=request.user)

    messages.success(request, 'The proposal was assigned successfully!')

    return redirect('teams:assign_to_members')


@login_required
@user_is_freelancer
def assigned_proposals_to_members(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, members__in=[request.user])
    assigned = team.assignteam.filter(
        proposal__status=Proposal.ACTIVE, is_assigned=True)

    context = {
        'team': team,
        'assigned': assigned,
    }
    return render(request, 'teams/assigned_task_to_members.html', context)


@login_required
@user_is_freelancer
def re_assign_proposal_to_any_member(request, assign_id, proposal_slug):
    team = get_object_or_404(
        Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    proposal = get_object_or_404(
        Proposal, slug=proposal_slug, team=team, status=Proposal.ACTIVE)
    assigned = get_object_or_404(
        AssignMember, team=team, id=assign_id, proposal=proposal)
    assignee = request.user.team_member.filter(
        pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)

    if request.method == 'POST':

        assignform = AssignForm(assignee, request.POST, instance=assigned)
        if assignform.is_valid():
            assignform.instance.assignor = request.user
            assignform.save()

            messages.info(
                request, f'Member - "{assignform.instance.assignor.short_name}" assigned successfuly')

            return redirect('teams:assign_to_members')

    else:
        assignform = AssignForm(assignee, instance=assigned)

    context = {
        'assignform': assignform,
        'team': team,
        'assigned': assigned,
    }
    return render(request, 'teams/reassign_to_member.html', context)


@login_required
@user_is_freelancer
def proposal_tracking(request,  proposal_slug, assign_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id,status=Team.ACTIVE, members__in=[request.user])
    proposal = get_object_or_404(Proposal, slug=proposal_slug, team=team)
    assigned = get_object_or_404(AssignMember, pk=assign_id, team=team)  # , is_tracked=True

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        tasks = request.POST.get('tasks')
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        total_minutes = (hours * 60) + minutes

        Tracking.objects.create(team=team, proposal=proposal, assigned=assigned, tasks=tasks,
                                minutes=total_minutes, created_by=request.user, created_at=date, is_tracked=True)
        messages.info(request, 'tracking logged successfuly')

        # return redirect('teams:team_single', team_id=team.id)

    context = {
        'team': team,
        'assigned': assigned,
        'proposal': proposal,
        'today': datetime.today(),
    }
    return render(request, 'teams/tracking.html', context)


@login_required
@user_is_freelancer
def modify_proposal_tracking(request,  proposal_slug, assign_id, tracking_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id,status=Team.ACTIVE, members__in=[request.user])
    proposal = get_object_or_404(Proposal, slug=proposal_slug, team=team)
    assigned = get_object_or_404(AssignMember, pk=assign_id, team=team)
    tracking = get_object_or_404(Tracking, pk=tracking_id, team=team, is_tracked=True)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        tasks = request.POST.get('tasks')
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        tracking.created_at = date
        tracking.tasks = tasks
        tracking.minutes = (hours * 60) + minutes
        tracking.save()

        messages.info(request, 'The changes was saved!')

        return redirect('teams:proposal_tracking', proposal_slug=proposal.slug, assign_id=assigned.id)

    hours, minutes = divmod(tracking.minutes, 60)
    tasks = Tracking.objects.values('tasks')
    context = {
        'team': team,
        'assigned': assigned,
        'proposal': proposal,
        'tracking': tracking,
        'today': datetime.today(),
        'hours': hours,
        'minutes': minutes,
        'tasks': tasks,
    }
    return render(request, 'teams/modify_tracking.html', context)


@login_required
@user_is_freelancer
def delete_proposal_tracking(request,  proposal_slug, assign_id, tracking_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id,status=Team.ACTIVE, members__in=[request.user])
    proposal = get_object_or_404(Proposal, slug=proposal_slug, team=team)
    assigned = get_object_or_404(AssignMember, pk=assign_id, team=team)
    tracking = get_object_or_404(
        Tracking, pk=tracking_id, team=team, is_tracked=True)
    tracking.delete()

    messages.info(request, 'The tracking activity was deleted successfully!')

    return redirect('teams:proposal_tracking', proposal_slug=proposal.slug, assign_id=assigned.id)


@login_required
def purchase_package(request, type):
    PayPalClient = PayPalClientConfig().paypal_public_key()
    stripe_public_key = StripeClientConfig().stripe_public_key()
    razorpay_public_key = RazorpayClientConfig().razorpay_public_key_id()
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    if not team.created_by == request.user:
        messages.error(
            request, 'You must be the owner of this team to access subscription page')
        return redirect("account:dashboard")

    package = ''

    if team:
        package = get_object_or_404(Package, type=type)

    return render(request, 'teams/purchase_package.html', {'package': package, 'stripe_public_key': stripe_public_key})


@login_required
def plans_activated(request):
    stripe_api = StripeClientConfig()
    error = ''
    check_package = Team.objects.filter(pk=request.user.freelancer.active_team_id,
        status=Team.ACTIVE, created_by=request.user, package__type='Team')
    if check_package:
        messages.error(request, 'You already have an active package.')
        return redirect("teams:packages")

    else:
        try:
            team = Team.objects.get(pk=request.user.freelancer.active_team_id,status=Team.ACTIVE)
            stripe.api_key = stripe_api.stripe_secret_key()
            subscription = stripe.Subscription.retrieve(team.stripe_subscription_id)
            product = stripe.Product.retrieve(subscription.plan.product)
            print(product.name)
            team.package_status = Team.ACTIVE
            team.package_expiry = datetime.fromtimestamp(subscription.current_period_end)
            team.package = Package.objects.get(type=product.name)
            print(team.package)
            team.save()

        except Exception:
            error = 'There something wrong. Please try again!'

    return render(request, 'teams/subscription_success.html', {'error': error})


@login_required
def packages(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    if not team.created_by == request.user:
        messages.error(request, 'Bad request. Page is restricted to non-founders')
        return redirect("account:dashboard")

    StripeClient = StripeClientConfig()
    packages = Package.objects.all()
    error = ''

    if request.GET.get('cancel_package', ''):
        try:
            default_package = Package.objects.get(is_default=True)
            team.package = default_package
            team.package_status = Team.DEFAULT
            team.package_expiry = datetime.now()
            team.save()
            
            stripe.api_key = StripeClient.stripe_secret_key
            stripe.Subscription.delete(team.stripe_subscription_id)
        except:
            error = 'Ooops! Something went wrong. Please try again later!'

    context = {
        'team': team,
        'error': error,
        'packages': packages,
        'stripe_pub_key': StripeClient.stripe_public_key
    }

    return render(request, 'teams/packages.html', context)


@login_required
def paypal_package_order(request):
    PayPalClient = PayPalClientConfig()
    body = json.loads(request.body)

    data = body["orderID"]
    team = get_object_or_404(
        Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
    paypal_request_order = OrdersGetRequest(data)
    response = PayPalClient.client.execute(paypal_request_order)
    SubscriptionItem.objects.create(
        team=team,
        subscriber=request.user,
        price=response.result.purchase_units[0].plan.amount.value,

        payment_method='PayPal',
        status=True
    )
