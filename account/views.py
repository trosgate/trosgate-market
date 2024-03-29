from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from django.contrib import auth, messages
from .forms import SearchTypeForm, MerchantRegisterForm, CustomerRegisterForm, UserLoginForm, TwoFactorAuthForm, PasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Country, Package, Merchant, TwoFactorAuth
from teams.models import Package as TeamPlan
from proposals.models import Proposal
from teams.models import Invitation, Team
from teams.forms import TeamCreationForm
from client.models import Client
from freelancer.models import Freelancer
from projects.models import Project
from notification.mailer import new_user_registration, two_factor_auth_mailer
from future.utilities import get_sms_feature, get_more_team_per_user_feature
from quiz.models import Quizes
from contract . models import Contract
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_control
from marketing.models import AutoTyPist
from django.conf import settings
from django.contrib.auth.hashers import check_password
from general_settings.fees_and_charges import get_contract_fee_calculator, get_application_fee_calculator, get_proposal_fee_calculator
from general_settings.models import Mailer
from general_settings.currency import get_base_currency_symbol
from .fund_exception import InvitationException
from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale
from freelancer.models import FreelancerAccount
from applications.application import ApplicationAddon
from contract.contract import BaseContract
from transactions.hiringbox import HiringBox
import copy
from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect
from contract.models import Contract
from .backend import CustomAuthBackend
from .permission import user_is_merchant
from django.db.models import When, Case, Q, Count, Value, CharField
from django.contrib.postgres.fields import ArrayField


@login_required
def remove_message(request):
    return HttpResponse("")


def subscribers(request):
    return render(request, 'account/subscriber.html', {})


@login_required
def Logout(request):
    '''
    This is manual method for user to logout.
    Custom session data stored in bucket need to persist.
    Rather than creating a cache, i create a deep copy since django calls flush() during logout
    User can now login to see data in bucket.
    All other session data not copied can be deleted.
    '''
    proposal_box = copy.deepcopy(HiringBox(request).hiring_box)
    application = copy.deepcopy(ApplicationAddon(request).applicant_box)
    contract = copy.deepcopy(BaseContract(request).contract_box)
    logout(request)

    request.user = None
    session = request.session
    session[settings.HIRINGBOX_SESSION_ID] = proposal_box
    session[settings.APPLICATION_SESSION_ID] = application
    session[settings.CONTRACT_SESSION_ID] = contract
    session.modified = True

    return redirect('account:homepage')


def autoLogout(request):
    '''
    This is automatic method for user logout.
    Custom session data stored in bucket need to persist.
    Rather than creating a cache, i create a deep copy since django calls flush() during logout.
    User can now login to see session specific data related to bucket.
    All other session data not copied can be deleted.
    '''    
    proposal_box = copy.deepcopy(HiringBox(request).hiring_box)
    application = copy.deepcopy(ApplicationAddon(request).applicant_box)
    contract = copy.deepcopy(BaseContract(request).contract_box)
    logout(request)

    request.user = None
    session = request.session
    session[settings.HIRINGBOX_SESSION_ID] = proposal_box
    session[settings.APPLICATION_SESSION_ID] = application
    session[settings.CONTRACT_SESSION_ID] = contract
    session.modified = True

    return redirect('account:homepage')


def homepage(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')
    
    base_currency = get_base_currency_symbol()
    pypist = AutoTyPist.objects.filter(is_active=True)
    packages = Package.objects.all()[0:3]
    proposals = Proposal.objects.filter(published=True).distinct()[0:12]   
    projects = Project.objects.filter(published=True, status='active', duration_time__gte=timezone.now()).distinct()[0:6]
    users = Freelancer.objects.filter(created=True).distinct()[0:12]
    searchform = SearchTypeForm()
    form_submitted = False

    if request.user.is_authenticated and not request.user.user_type == Customer.ADMIN:
        messages.info(request, f'Welcome back {request.user.short_name}')
        return redirect('account:dashboard')

    if request.user.is_authenticated and request.user.user_type == Customer.ADMIN:
        messages.info(request, f'Welcome back {request.user.short_name}')
        return redirect('/admin')

    context = {
        'proposals': proposals,
        'projects': projects,
        'packages': packages,
        'pypist': pypist,
        'users': users,
        'base_currency': base_currency,
        'searchform': searchform,
        'home_layout': request.site,
        'form_submitted': form_submitted,
    }
    if request.parent_site:
        return render(request, 'homepage.html', context)
    else:
        return render(request, 'merchant_home.html', context)


def searchtype(request):
    if request.POST.get('action') == 'searching-type':
        searchvalue = str(request.POST.get('searchVal'))
        return JsonResponse({'searchvalue':searchvalue})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginView(request):

    # Admin is exempted from two step verification via sms
    # Otherwise if there is bug in mail sending, admin is also lock out 
    # TODO to have a token authenticator separate for admin and staffs
    
    if request.user.is_authenticated:
        messages.info(request, f'Welcome back {request.user.get_short_name()}')
        return redirect('account:dashboard')
      
    session = request.session
    loginform = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
       
        if user is not None and user.site == request.site:

            if user.is_freelancer and get_sms_feature():
                
                if "twofactoruser" not in session:
                    session["twofactoruser"] = {"user_pk": user.pk}
                    session.modified = True
                    return redirect('account:two_factor_auth')

                return redirect('account:two_factor_auth')

            elif user.is_freelancer and not get_sms_feature():
                
                login(request, user)

                messages.info(request, f'Welcome back {user.get_short_name()}')

                return redirect('account:dashboard')

            elif user.is_client and get_sms_feature():

                if "twofactoruser" not in session:
                    session["twofactoruser"] = {"user_pk": user.pk}
                    session.modified = True
                    return redirect('account:two_factor_auth')

                return redirect('account:two_factor_auth')

            elif user.is_client and not get_sms_feature():            
                
                login(request, user)

                messages.info(request, f'Welcome back {user.get_short_name()}')

                return redirect('account:dashboard')

            elif user.is_merchant and get_sms_feature():
                if "twofactoruser" not in session:
                    session["twofactoruser"] = {"user_pk": user.pk}
                    session.modified = True
                    return redirect('account:two_factor_auth')

                return redirect('account:two_factor_auth')

            elif user.is_merchant and not get_sms_feature():
                
                login(request, user)

                messages.info(request, f'Welcome back {user.get_short_name()}')

                return redirect('account:dashboard')  
            
            else:
                messages.error(request, f'Invalid email or Password.')

        else:
            messages.error(request, f'Invalid email or Password.')
    else:
        loginform = UserLoginForm()

    context = {
        'loginform': loginform
    }
    if request.parent_site:
        return render(request, "account/parent_login.html", context)
    else:
        return render(request, "account/merchant_login.html", context)


def two_factor_auth(request):

    if "twofactoruser" not in request.session:
        return redirect("account:login")

    try:
        returned_user_pk = request.session["twofactoruser"]["user_pk"]
        returned_user = TwoFactorAuth.objects.get(user__pk=returned_user_pk, user__is_active=True)
        pass_code = returned_user.pass_code
        user = Customer.objects.get(pk=returned_user_pk, is_active=True)
    except:
        returned_user=None
        user=None
        return redirect("account:login")

    twofactorform = TwoFactorAuthForm(request.POST or None)

    if not request.POST:
        try:
            two_factor_auth_mailer(user, pass_code)
            messages.info(request, f'Token sent to your email')
        except:
            print('Activation token not sent')
   
    if twofactorform.is_valid():
        received_code = twofactorform.cleaned_data['pass_code']

        if pass_code == received_code:
            returned_user.save()

            login(request, user)

            messages.info(request, f'Welcome back {request.user.get_short_name()}')

            return redirect("account:dashboard")

        messages.error(request, 'Invalid code!')

    context = {
        'twofactorform': twofactorform
    }
    return render(request, "account/two_factor_auth.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account_register(request):
    if request.user.is_authenticated:
        messages.info(request, f'Welcome back {request.user.short_name}')
        return redirect('account:dashboard')

    if request.user.is_authenticated and request.user.user_type == Customer.ADMIN:
        messages.info(request, f'Welcome back {request.user.short_name}')

        return redirect('/admin')

    supported_country = Country.objects.filter(supported=True)

    if request.method == 'POST':
        regform = CustomerRegisterForm(supported_country, request.POST or None)
        if regform.is_valid():
            regform.save()
            return render(request, 'account/registration/register_email_confirm.html', {'success': 'success'})

    else:
        regform = CustomerRegisterForm(supported_country)
    return render(request, 'account/register.html', {'regform': regform})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_merchant(request, type):
    if request.user.is_authenticated and request.user.user_type == Customer.MERCHANT:
        messages.info(request, f'Welcome back {request.user.get_short_name}')
        return redirect('account:dashboard')

    if request.user.is_authenticated and request.user.user_type == Customer.ADMIN:
        messages.info(request, f'Welcome back {request.user.get_short_name}')

        return redirect('/admin')

    package = get_object_or_404(Package, type=type)
    supported_country = Country.objects.filter(supported=True)

    if request.method == 'POST':
        regform = MerchantRegisterForm(supported_country, request.POST or None)
        if regform.is_valid():
            regform.save()
            return render(request, 'account/registration/register_email_confirm.html', {'success': 'success'})

    else:
        regform = MerchantRegisterForm(supported_country)
    return render(request, 'account/subscription.html', {'regform': regform, 'package':package,})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_dashboard(request):
    '''
    function for getting freelancer properties
    function for getting client properties
    we create new team within dashboard
    '''
    package = None
    contracts=None
    proposals=None
    msg = ''

    if request.user.is_freelancer:
        user_active_team = Team.objects.filter(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE).first()
        contracts = Contract.objects.filter(team=user_active_team, reaction=Contract.AWAITING)
        proposals = Proposal.objects.filter(team=user_active_team)
        freelancer_profile = Freelancer.objects.filter(created=True, user__id=request.user.id).first()
        open_projects = Project.objects.filter(status=Project.ACTIVE, duration_time__gte=timezone.now())[:10]
        quizz = Quizes.objects.filter(is_published=True)[:10]
        teams = request.user.team_member.all().exclude(pk=request.user.freelancer.active_team_id)
        belong_to_more_than_one_team = request.user.team_member.filter(status=Team.ACTIVE).count() > 1

        package=TeamPlan.objects.get_or_create(merchant=request.merchant,type=TeamPlan.BASIC)[0]

        base_currency = get_base_currency_symbol()

        if request.method == 'POST' and get_more_team_per_user_feature():
            teamform = TeamCreationForm(request.POST or None)
            if teamform.is_valid():
                try:
                    Team.create_team_with_member(
                        title=teamform.cleaned_data['title'],
                        notice=teamform.cleaned_data['notice'],
                        merchant = request.merchant,
                        created_by=request.user,
                        package=package,
                    )
                    
                    messages.success(request, f'The Team was created successfully!')
                except Exception as e:
                    msg = str(e)
                    messages.error(request, f'Sorry! {msg}')
                    pass

                return redirect('account:dashboard')
            
            messages.error(request, f'Sorry! an error occured. Please try in few time')
                        
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
            'teams': teams,
            'base_currency': base_currency,
        }
        return render(request, 'account/user/freelancer_dashboard.html', context)


    if request.user.is_client:
        client_profile = Client.objects.get(user=request.user)
        proposals = Proposal.objects.filter(status=Proposal.ACTIVE)
        open_projects = Project.objects.filter(created_by=request.user, status=Project.ACTIVE, duration_time__gte=timezone.now())
        closed_projects = Project.objects.filter(created_by=request.user, status=Project.ACTIVE, reopen_count=0, duration_time__lt=timezone.now())

        # open_projects = Project.objects.filter(
        #     Q(created_by=request.user, status=Project.ACTIVE, duration_time__gte=timezone.now()) |
        #     Q(created_by=request.user, status=Project.ACTIVE, reopen_count=0, duration_time__lt=timezone.now())
        # )

        contracts = Contract.objects.filter(
            Q(created_by=request.user)|
            Q(client__email__iexact=request.user.email)
        ).exclude(reaction = Contract.PAID)
        base_currency = get_base_currency_symbol()
        context = {
            'open_projects': open_projects,
            'closed_projects': closed_projects,
            'proposals': proposals,
            'contracts': contracts,
            'client_profile': client_profile,
            'base_currency': base_currency,
        }
        return render(request, 'account/user/client_dashboard.html', context)


    if request.user.is_merchant:
        
        merchant_profile = get_object_or_404(Merchant, pk=request.user.active_merchant_id, members__in=[request.user])
 
        context = {
            'merchant_profile': merchant_profile,

        }
        return render(request, 'account/user/merchant_dashboard.html', context)


    if request.user.is_admin:
        messages.info(request, f'Welcome back {request.user.get_short_name()}')

        return redirect('/admin/')


@login_required
@user_is_merchant
def merchant_user(request):
    user_choice  = request.GET.get('usertype', 'all_users')
    request.session["usertype"] = user_choice        
    user_choices = request.session.get('usertype', user_choice)

    print(user_choices)
    merchant_user = Q(user_type=Customer.FREELANCER) | Q(user_type=Customer.CLIENT)
    merchant_only = Q(user_type=Customer.MERCHANT)
    merchant_users = Customer.objects.filter(
        active_merchant_id=request.merchant.pk
    ).annotate(
        user_type_chosen = Case(
            When(Q(merchant_user), then=Value('all_users')),
            When(merchant_only, then=Value('merchant')),
            default=Value('all_users'),
            output_field=CharField()
        )
    )
    merchant_users = merchant_users.filter(user_type_chosen=user_choice)

    context = {
        'merchant_users': merchant_users,
    }
    if request.htmx:
        return render(request, 'account/partials/merchant_users.html', context)
    return render(request, 'account/user/merchant_user.html', context)


@login_required
@user_is_merchant
def block_or_unblock(request):
    user_id = request.GET.get('merchant_users')
    user_choice = request.session.get('usertype', 'all_users')
    myuser = get_object_or_404(Customer, active_merchant_id=request.merchant.pk, pk=user_id)
    
    if myuser.is_active == True:
        myuser.is_active = False
        myuser.save()
    else:
        myuser.is_active = True
        myuser.save()

    merchant_user = Q(user_type=Customer.FREELANCER) | Q(user_type=Customer.CLIENT)
    merchant_only = Q(user_type=Customer.MERCHANT)
    merchant_users = Customer.objects.filter(
        active_merchant_id=request.merchant.pk
    ).annotate(
        user_type_chosen = Case(
            When(Q(merchant_user), then=Value('all_users')),
            When(merchant_only, then=Value('merchant')),
            default=Value('all_users'),
            output_field=CharField()
        )
    )
    merchant_users = merchant_users.filter(user_type_chosen=user_choice)

    context = {
        'merchant_users': merchant_users,
    }
    return render(request, 'account/partials/merchant_users.html', context)














































































