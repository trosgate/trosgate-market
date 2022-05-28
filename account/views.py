from django.http import HttpResponse, HttpResponseRedirect
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib import auth, messages
from .forms import CustomerRegisterForm, UserLoginForm, TwoFactorAuthForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Country, TwoFactorAuth
from proposals.models import Proposal
from teams.models import Invitation, Team, Package
from teams.forms import TeamCreationForm
from client.models import Client
from freelancer.models import Freelancer
from django.utils.text import slugify
from projects.models import Project
from . utilities import new_user_registration, send_verification_sms
from future.utilities import get_sms_feature, get_more_team_per_user_feature
from teams.utilities import send_new_team_email
from teams.controller import max_proposals_allowable_per_team
from quiz.models import Quizes
from contract . models import InternalContract
from datetime import datetime, timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from general_settings.decorators import confirm_recaptcha
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
# prevent back button on browser after form submission
from django.views.decorators.cache import cache_control
from marketing.models import AutoTyPist
from django.conf import settings
from general_settings.gateways import PayPalClientConfig
from django.contrib.auth.hashers import check_password
from general_settings.fees_and_charges import get_contract_fee_calculator, get_application_fee_calculator, get_proposal_fee_calculator
from general_settings.models import Mailer



def autoLogout(request):
    logout(request)
    request.user = None
    messages.info(
        request, "The system has logged you out and your Account is now secure")
    return redirect('account:homepage')


def homepage(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    pypist = AutoTyPist.objects.filter(is_active=True)
    packages = Package.objects.all()[0:3]
    proposals = Proposal.objects.filter(
        status=Proposal.ACTIVE, published=True)[0:12]
    projects = Project.objects.filter(
        status=Project.ACTIVE, published=True)[0:6]

    context = {
        'proposals': proposals,
        'projects': projects,
        'packages': packages,
        'pypist': pypist,
    }
    return render(request, 'homepage.html', context)


# @confirm_recaptcha
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginView(request):

    session = request.session
    if request.user.is_authenticated:
        return redirect('account:two_factor_auth')
    
    loginform = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        # Admin is exempted from two step verification
        # Otherwise if there is server error in sms sending, admin is also lock out 
        if user is not None and user.user_type == Customer.ADMIN and user.is_active == True:
             
            login(request, user)

            messages.info(request, f'Welcome back {user.short_name}')

            return redirect('/admin')

        # Checks for freelancer and redirect to 2FA or otherwise
        if user is not None and user.user_type == Customer.FREELANCER and user.is_active == True and get_sms_feature():

            if "twofactoruser" not in session:
                session["twofactoruser"] = {"user_pk": user.pk}
                session.modified = True
                return redirect('account:two_factor_auth')

            return redirect('account:two_factor_auth')

        if user is not None and user.user_type == Customer.FREELANCER and user.is_active == True:
            
            login(request, user)

            messages.info(request, f'Welcome back {user.short_name}')

            return redirect('account:dashboard')            
        
        # return redirect("account:login")

        if user is not None and user.user_type == Customer.CLIENT and user.is_active == True and get_sms_feature():

            if "twofactoruser" not in session:
                session["twofactoruser"] = {"user_pk": user.pk}
                session.modified = True
                return redirect('account:two_factor_auth')

            return redirect('account:two_factor_auth')


        if user is not None and user.user_type == Customer.CLIENT and user.is_active == True:            
            
            login(request, user)

            messages.info(request, f'Welcome back {user.short_name}')

            return redirect('account:dashboard')            
        
    else:
        loginform = UserLoginForm()
            
    context = {
        'loginform': loginform
    }
    return render(request, "account/login.html", context)


def two_factor_auth(request):

    if "twofactoruser" not in request.session:
        return redirect("account:login")

    returned_user_pk = request.session["twofactoruser"]["user_pk"]

    returned_user = TwoFactorAuth.objects.get(user__pk=returned_user_pk, user__is_active=True)
    pass_code = returned_user.pass_code
    user = Customer.objects.get(pk=returned_user_pk, is_active=True)

    twofactorform = TwoFactorAuthForm(request.POST or None)

    if not request.POST:
        send_verification_sms(user, pass_code, user.phone)
   
    if twofactorform.is_valid():
        received_code = twofactorform.cleaned_data['pass_code']

        if pass_code == received_code:
            returned_user.save()

            login(request, user)

            messages.info(request, f'Welcome back {request.user.short_name}')

            invitation = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)

            if invitation:
                messages.info(
                    request, f'Hi "{request.user.short_name}", you have a pending team invite. Please check your inbox for verification code')

            return redirect("account:dashboard")

        messages.error(request, 'Invalid email or password!')

    context = {
        'twofactorform': twofactorform
    }
    return render(request, "account/two_factor_auth.html", context)



# @confirm_recaptcha
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account_register(request):
    if request.user.is_authenticated:
        messages.info(request, f'Welcome back {request.user.short_name}')
        return redirect('account:dashboard')

    if request.user.is_authenticated and user.user_type == Customer.ADMIN:
        messages.info(request, f'Welcome back {request.user.short_name}')

        return redirect('/admin')

    supported_country = Country.objects.filter(supported=True)
    if request.method == 'POST':
        regform = CustomerRegisterForm(supported_country, request.POST)
        if regform.is_valid():  # and request.recaptcha_is_valid:
            user = regform.save(commit=False)
            user.email = regform.cleaned_data['email']
            user.set_password(regform.cleaned_data['password1'])
            user.is_active = False
            user.save()

            to_email = user.email
            new_user_registration(user, to_email)

            return redirect('account:login')

    else:
        regform = CustomerRegisterForm(supported_country)
    return render(request, 'account/register.html', {'regform': regform})


__all__ = ['new_user_registration']

# def states(request):
#     country = request.GET.get('country')
#     states= State.objects.filter(country=country)
#     return render(request, 'account/partials/states.html', {'states': states})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, request.user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('account:login')

    else:
        return render(request, 'account/registration/register_activation_invalid.html')


@login_required
def user_dashboard(request):
    '''
    function for getting freelancer properties

    function for getting client properties

    we create new team within dashboard
    '''
    package = ''
    if request.user.user_type == Customer.FREELANCER and request.user.is_active == True:
        user_active_team = Team.objects.get(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
        freelancer_profile = Freelancer.objects.get(user__id=request.user.id)
        open_projects = Project.objects.filter(status=Project.ACTIVE, duration__gt=datetime.now())[:10]
        contracts = user_active_team.internalcontractteam.filter(status=InternalContract.PENDING)[:10]
        proposals = user_active_team.proposalteam.all()[:12]
        quizz = Quizes.objects.filter(is_published=True)[:10]
        teams = request.user.team_member.filter(status=Team.ACTIVE).exclude(pk=request.user.freelancer.active_team_id)
        belong_to_more_than_one_team = request.user.team_member.filter(status=Team.ACTIVE).count() > 1

        # mailer = Mailer.objects.get('**kwargs')

        if request.method == 'POST' and get_more_team_per_user_feature():
            teamform = TeamCreationForm(request.POST or None)
            try:
                package=Package.objects.get(id=1)
            except:
                pass
            if teamform.is_valid():
                team = teamform.save(commit=False)
                team.created_by = request.user
                team.package = package
                team.slug = slugify(team.title)
                team.save()
                team.members.add(request.user)

                # email = team.created_by.email
                freelancer = request.user.freelancer
                freelancer.active_team_id = team.id
                freelancer.save()

                # Invitation.objects.create(team=team, email=email, status = Invitation.INVITED)

                messages.success(request, 'The team was created successfully!')
                # send_new_team_email(email, team)

                return redirect('account:dashboard')

        else:
            teamform = TeamCreationForm()
        context = {
            'proposals': proposals,
            'open_projects': open_projects,
            'freelancer_profile': freelancer_profile,
            'teamform': teamform,
            'quizz': quizz,
            'contracts': contracts,
            'belong_to_more_than_one_team': belong_to_more_than_one_team,
            'max_proposals_per_team': max_proposals_allowable_per_team(request),
            'teams': teams,
        }
        return render(request, 'account/user/freelancer_dashboard.html', context)

    if request.user.user_type == Customer.CLIENT and request.user.is_active == True:
        client_profile = Client.objects.get(user=request.user)
        proposals = Proposal.objects.filter(status=Proposal.ACTIVE)
        open_projects = Project.objects.filter(created_by=request.user, status=Project.ACTIVE, duration__gt=datetime.now())
        closed_projects = Project.objects.filter(created_by=request.user, status=Project.ACTIVE, duration__lt=datetime.now())
        contracts = InternalContract.objects.filter(status=InternalContract.PENDING, created_by=request.user)[:10]

        context = {
            'open_projects': open_projects,
            'closed_projects': closed_projects,
            'proposals': proposals,
            'contracts': contracts,
            'client_profile': client_profile,
        }
        return render(request, 'account/user/client_dashboard.html', context)
    
    if request.user.user_type == Customer.ADMIN and request.user.is_active == True:
        messages.info(request, f'Welcome back {request.user.short_name}')

        return redirect('/admin')