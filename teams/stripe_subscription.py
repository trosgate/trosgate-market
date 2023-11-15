
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
from transactions.models import SubscriptionItem
from payments.checkout.stripe import StripeClientConfig
from django.contrib import messages
from django.utils import timezone


@login_required
def stripe_subscription_checkout_session(request):
    # data = json.loads(request.body)
    # team_id = data['team_id']
    
    team = Team.objects.filter(pk=request.user.freelancer.active_team_id, created_by=request.user, status=Team.ACTIVE)
    if not team:
        error_message = messages.error(request, 'Bad request. Let the team owner subscribe')
        return HttpResponse({'error_message': error_message})
         
    site_url =  'http://' + str(get_current_site(request))

    stripe_obj = StripeClientConfig()
    stripe.api_key = stripe_obj.stripe_secret_key()    
    price_id = stripe_obj.stripe_subscription_price_id()
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.freelancer.active_team_id,
            success_url='%s%s?session_id={CHECKOUT_SESSION_ID}' % (site_url, reverse('teams:package_success')),
            cancel_url='%s%s' % (site_url, reverse('teams:packages')),
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                }
            ],
            mode='subscription',
            
        )

        return JsonResponse({'sessionId': checkout_session})
    except Exception as e:
        return JsonResponse({'error': str(e)})

