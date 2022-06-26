
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
from . models import Team, Package
from transactions.models import SubscriptionItem
from general_settings.gateways import RazorpayClientConfig
from django.contrib import messages
from django.utils import timezone
from general_settings.currency import get_base_currency_symbol, get_base_currency_code

# razorpay_plan = razorpay_api.razorpay_subscription_price_id()

@login_required
def razorpay_subscription_checkout_session(request):
    team = Team.objects.filter(pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
    if not team:
        error_message = messages.error(request, 'Bad request. Let the team owner subscribe')
        return HttpResponse({'error_message': error_message})

    razorpay_api = RazorpayClientConfig()
    razorpay_client = razorpay_api.get_razorpay_client()
    razorpay_plan_id = razorpay_api.razorpay_subscription_price_id()
    base_currency_code = get_base_currency_code()
    try:
        team = Team.objects.get(pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)        
        razorpay_plan = razorpay_client.plan.fetch(razorpay_plan_id)

        razorpay_subscription= razorpay_client.subscription.create({
        'plan_id': razorpay_plan_id,
        'customer_notify': 1,
        'total_count': 1,
        'quantity': 1,
        # 'start_at': timezone.now().timestamp(),
        'notes': {'key1': 'value3', 'key2': 'value2'}
        }) 

        new_subscription = razorpay_client.subscription.fetch(razorpay_subscription['id'])  
                 
        team.razorpay_plan_item = razorpay_plan['item']['id']
        team.razorpay_subscription_id = razorpay_subscription['id']
        team.razorpay_payment_url = razorpay_subscription['short_url']
        team.save()


        print('razorpay_order_note', razorpay_subscription['short_url'])
        print('new_subscription', new_subscription)


        context={
            'currency':base_currency_code, 
            # 'amount': (purchase.salary_paid), 
            'razorpay_subscription': razorpay_subscription
        }
        
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({'error': str(e)})



@login_required
# @user_is_client
def razorpay_subscription_callback(request):
    razorpay_client = RazorpayClientConfig().get_razorpay_client()
    if request.POST.get('action') =='razorpay-subscription':
        razorpay_order_key = request.POST.get('orderid')
        razorpay_payment_id = request.POST.get('paymentid')
        razorpay_signature = request.POST.get('signature')
        
        data ={
            'razorpay_order_id': razorpay_order_key,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        team = Team.objects.get(razorpay_order_key=razorpay_order_key, status=Team.ACTIVE)
        team.razorpay_payment_id = razorpay_payment_id
        team.razorpay_signature = razorpay_signature
        team.save()

        signature = razorpay_client.utility.verify_payment_signature(data)
        # if signature == True:
        #     purchase.status = Purchase.SUCCESS
        #     purchase.save()

        return JsonResponse({'Perfect':'All was successful',})