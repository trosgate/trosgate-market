
import sys
import os
import json
import stripe
from django.contrib.sites.shortcuts import get_current_site
from general_settings.models import WebsiteSetting
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Team
from account.models import Package
from .utilities import get_expiration
from transactions.models import SubscriptionItem
from general_settings.gateways import RazorpayClientConfig
from django.contrib import messages
from django.utils import timezone
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
import time
from datetime import timedelta


@login_required
def razorpay_subscription_checkout_session(request):
    razorpay_api = RazorpayClientConfig()
    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_plan_id = razorpay_api.razorpay_subscription_price_id()
    base_currency_code = get_base_currency_code()

    # time_now = timezone.now() + timedelta(minutes=2)
    # start_at = int((time.mktime(time_now.timetuple())))

    # expiry = get_expiration()
    # expire_by = int((time.mktime(expiry.timetuple())))
    try:
        package = Package.objects.get(is_default=False, type='Team')
        amount = int(package.price * 100)
        team = Team.objects.get(pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)        
        razorpay_subscription= razorpay_client.subscription.create({
        'plan_id': razorpay_plan_id,
        'customer_notify': 1,
        'total_count': 1,
        'quantity': 1,
        # start_at:
        # expire_by:
        'notes': {'key1': f'Subscription by {team.title}'}
        }) 
                
        # team.razorpay_plan_item = razorpay_plan['item']['id']
        team.razorpay_subscription_id = razorpay_subscription['id']
        team.razorpay_payment_url = razorpay_subscription['short_url']
        team.save()

        context={
            'currency':base_currency_code, 
            'amount': amount, 
            'description': razorpay_subscription['notes']['key1'],
            'razorpay_subscription_id': razorpay_subscription['id']
        }
        
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@login_required
# @user_is_client
def razorpay_subscription_webhook(request):
    razorpay_client = RazorpayClientConfig().get_razorpay_client()

    if request.POST.get('action') =='razorpay-subscription':
        razorpay_subscription_id = request.POST.get('subscriptionID')
        razorpay_payment_id = request.POST.get('paymentID')
        razorpay_signature = request.POST.get('signature')
        print('razorpay_subscription_id:', razorpay_subscription_id)
        print('razorpay_payment_id:', razorpay_payment_id)
        print('razorpay_signature:', razorpay_signature)
        data ={
            'razorpay_subscription_id': razorpay_subscription_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        signature = razorpay_client.utility.verify_subscription_payment_signature(data)
        print('signature;', signature)
        if signature == True:
            try:
                package = Package.objects.get(is_default=False, type='Team')
                team = Team.objects.get(razorpay_subscription_id=razorpay_subscription_id, status=Team.ACTIVE)
                team.razorpay_payment_id = razorpay_payment_id
                team.package = package
                team.package_status = Team.ACTIVE
                team.package_expiry = get_expiration()
                team.save()
                
                SubscriptionItem.objects.create(    
                    team=team,
                    customer_id = team.razorpay_payment_id,
                    subscription_id=team.razorpay_subscription_id,
                    payment_method='Razorpay', 
                    price=package.price, 
                    created_at = timezone.now(),
                    activation_time = timezone.now(),
                    expired_time = get_expiration(),
                    status = True,
                )
            except:
                pass

        return JsonResponse({'Perfect':'All was successful',})


# # Python SDK: https://github.com/razorpay/razorpay-python
# import razorpay
# client = razorpay.Client(auth=("[YOUR_KEY_ID]", "[YOUR_KEY_SECRET]"))

# client.utility.verify_webhook_signature(webhook_body, webhook_signature, webhook_secret)
# webhook_body should be raw webhook request body






