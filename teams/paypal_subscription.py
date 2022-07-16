import json
import requests
from django.contrib.sites.shortcuts import get_current_site
from general_settings.models import WebsiteSetting
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Team, Package
from transactions.models import SubscriptionItem
from general_settings.gateways import PayPalClientConfig, get_gateway_environment
from django.contrib import messages
from django.utils import timezone
from .utilities import get_expiration
from django.shortcuts import render, redirect, get_object_or_404


def get_paypal_subscription_url():
    '''
    This function will dynamically switch path to sandbox or live
    '''
    url = ''
    if get_gateway_environment() == True:
        # Sandbox url for testing
        url = 'https://api-m.sandbox.paypal.com/'
    else: 
        # Live url for production
        url = 'https://api-m.paypal.com/'

    return url

def get_subscription_access_token():
    paypalClient = PayPalClientConfig()
    data = {'grant_type':'client_credentials'}
    headers = {'Accept':'application/json', 'Accept-Language':'en_US'}
    url = get_paypal_subscription_url()
    url_prefix = 'v1/oauth2/token'
    url_full_path = f'{url}{url_prefix}'
    data_request = requests.post(url_full_path, auth=(paypalClient.paypal_public_key(), paypalClient.paypal_secret_key()), headers=headers, data=data).json()
    access_token = data_request['access_token']
    return access_token

def activate_paypal_subscription(request):
    body = json.loads(request.body)
    package_id = body["subscriptionID"]
    client_reference_id = body["customerID"]

    access_token = get_subscription_access_token()
    bearer_token = 'Bearer ' + access_token
    headers = {'Content-Type':'application/json', 'Authorization':bearer_token}

    url = get_paypal_subscription_url()
    url_prefix = 'v1/billing/subscriptions/'
    url_full_path =  f'{url}{url_prefix}{package_id}'
    data = requests.get(url_full_path, headers=headers).json()

    subscription_id = data['id']
    status = data['status']
    start_time = data['start_time']
    customer_id = data['subscriber']['payer_id']
    outstanding_balance = float(data['billing_info']['outstanding_balance']['value'])
    remaining_balance = int(outstanding_balance)
    next_billing_time = data['billing_info']['next_billing_time']

    error = ''
    if status == "ACTIVE" and remaining_balance == 0 and package_id == subscription_id:
        try:
            package = Package.objects.get(is_default=False, type='Team')
            team = Team.objects.get(pk=client_reference_id)
            team.paypal_customer_id = customer_id
            team.paypal_subscription_id = subscription_id
            team.package = package
            team.package_status = Team.ACTIVE
            team.package_expiry = next_billing_time
            team.save()
        
            SubscriptionItem.objects.create(    
                team=team,
                customer_id = team.paypal_customer_id,
                subscription_id=team.paypal_subscription_id,
                payment_method='PayPal', 
                price=package.price, 
                created_at = start_time,
                activation_time = start_time,
                expired_time = next_billing_time,
                status = True,
            )
        except Exception as e:
            error = str(e)

    return JsonResponse({'Success':'it worked', 'error':error})


def deactivate_paypal_subscription(request):
    team = Team.objects.get(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, package_status=Team.ACTIVE)

    if request.GET.get('cancel_package', ''):
        try:
            url = get_paypal_subscription_url()
            access_token = get_subscription_access_token()
            bearer_token = 'Bearer ' + access_token
            headers = {'Content-Type':'application/json', 'Authorization':bearer_token}

            body = {'reason':'Subscription cycle completed'}

            url = get_paypal_subscription_url() + 'v1/billing/subscriptions/' + team.paypal_subscription_id  + '/cancel'
            data = requests.post(url, headers=headers, data=body).json()
            print('data:::',data)
            print('data:::',data['status_code'])

            default_package = Package.objects.get(is_default=True)
            team.package = default_package
            team.package_status = Team.DEFAULT
            team.package_expiry = timezone.now()
            team.save()

            # SubscriptionItem.objects.filter(subscription_id=team.paypal_subscription_id).update()
                        
        except:
            error = 'Ooops! Something went wrong. Please try again later!'


    

@login_required
def packages(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE, package_status=Team.ACTIVE)
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