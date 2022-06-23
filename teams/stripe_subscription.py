
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
from general_settings.gateways import StripeClientConfig
from django.contrib import messages
from django.utils import timezone


@login_required
def stripe_subscription_checkout_session(request):
    data = json.loads(request.body)
    team_id = data['team_id']
    
    team = Team.objects.filter(pk=team_id, created_by=request.user, status=Team.ACTIVE)
    if not team:
        error_message = messages.error(request, 'Bad request. Let the team owner subscribe')
        return HttpResponse({'error_message': error_message})
         
    site_url =  'http://' + str(get_current_site(request))

    stripe_obj = StripeClientConfig()
    stripe.api_key = stripe_obj.stripe_secret_key()    
    price_id = stripe_obj.stripe_subscription_price_id()
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=team_id,
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


# @csrf_exempt
# def stripe_subscription_webhook(request):
#     stripe_obj = StripeClientConfig()
#     stripe.api_key = stripe_obj.stripe_secret_key()
#     webhook_key = stripe_obj.stripe_webhook_key()

#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     payload = request.body
#     print(payload)
#     event = None

#     # if "package" in request.path:

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, webhook_key
#         )
#     except ValueError as e:
#         # returns Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # returns Invalid signature
#         return HttpResponse(status=400)

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         team = Team.objects.get(pk=session.get('client_reference_id'))
#         team.stripe_customer_id = session.get('customer')
#         team.stripe_subscription_id = session.get('subscription')
#         team.save()

#         print('Team %s subscribed to a plan' % team.title)

#     return HttpResponse(status=200)








@csrf_exempt
def init_stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': stripe_api.stripe_public_key()}
        return JsonResponse(stripe_config, safe=False)


@login_required
def create_stripe_checkout_session(request):
    site_url = 'http://127.0.0.1:8000'
    price_id = stripe_api.stripe_subscription_price_id()
    stripe.api_key = stripe_api.stripe_secret_key()

    if request.method == 'GET':

        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.freelancer.active_team_id,
                success_url='%s%s?session_id={CHECKOUT_SESSION_ID}' % (site_url, reverse('teams:package_success')),
                cancel_url='%s%s' % (site_url, reverse('teams:packages')),
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = stripe_api.stripe_secret_key()
#     webhook_key = stripe_api.stripe_webhook_key()

#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     payload = request.body
#     print(payload)
#     event = None

#     # if "package" in request.path:

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, webhook_key
#         )
#     except ValueError as e:
#         # returns Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # returns Invalid signature
#         return HttpResponse(status=400)

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         team = Team.objects.get(pk=session.get('client_reference_id'))
#         team.stripe_customer_id = session.get('customer')
#         team.stripe_subscription_id = session.get('subscription')
#         team.save()

#         print('Team %s subscribed to a plan' % team.title)

#     return HttpResponse(status=200)
