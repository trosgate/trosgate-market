from django.shortcuts import render,get_object_or_404, redirect
from account.models import Customer
from freelancer.models import Freelancer, FreelancerAccount, FreelancerAction
from django.contrib.auth.decorators import login_required
from account.permission import user_is_merchant
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from payments.models import (
    PaymentGateway, 
    MerchantAPIs,
    PaymentAccount, 
    PaymentRequest
)
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from general_settings.currency import get_base_currency_symbol
from payments.forms import (
    StripeMerchantForm, 
    PayPalMerchantForm, 
    FlutterwaveMerchantForm, 
    RazorpayMerchantForm, 
    MTNMerchantForm
)
from django.contrib import messages
# from payments.checkout_card import CreditCard


@login_required
@user_is_merchant
def payment_settings(request):
    gateways = PaymentGateway.objects.filter(status=True).exclude(name='balance')
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    stripeform = StripeMerchantForm(request.POST or None, instance=merchant_api)
    paypalform = PayPalMerchantForm(request.POST or None, instance=merchant_api)
    flutterwaveform = FlutterwaveMerchantForm(request.POST or None, instance=merchant_api)
    razorpayform = RazorpayMerchantForm(request.POST or None, instance=merchant_api)
    mtnform = MTNMerchantForm(request.POST or None, instance=merchant_api)
    context = {
        'merchant_api': merchant_api,
        'stripeform': stripeform,
        'paypalform': paypalform,
        'flutterwaveform': flutterwaveform,
        'razorpayform': razorpayform,
        'mtnform': mtnform,
        'gateways': gateways,
    }
    return render(request, "merchants/payment_settings.html", context)


@login_required
@user_is_merchant
def add_or_remove_gateway(request):
    gateway_pk = request.POST.get('mygateway')

    try:
        gateway = PaymentGateway.objects.get(pk=gateway_pk, status=True)
    except MerchantAPIs.DoesNotExist:
        gateway = None

    try:
        merchant_api = MerchantAPIs.objects.get(merchant=request.merchant)
    except MerchantAPIs.DoesNotExist:
        merchant_api = None

    if merchant_api and merchant_api.stripe_active == True and gateway and gateway.name == 'stripe':
        merchant = request.merchant
        if gateway in merchant.gateways.all():
            merchant.gateways.remove(gateway)
        else:
            merchant.gateways.add(gateway)

    elif merchant_api and merchant_api.paypal_active == True and gateway and gateway.name == 'paypal':
        merchant = request.merchant
        if gateway in merchant.gateways.all():
            merchant.gateways.remove(gateway)
        else:
            merchant.gateways.add(gateway) 
    
    elif merchant_api and merchant_api.flutterwave_active == True and gateway and gateway.name == 'flutterwave':
        merchant = request.merchant
        if gateway in merchant.gateways.all():
            merchant.gateways.remove(gateway)
        else:
            merchant.gateways.add(gateway) 
    
    elif merchant_api and merchant_api.razorpay_active == True and gateway and gateway.name == 'razorpay':
        merchant = request.merchant
        if gateway in merchant.gateways.all():
            merchant.gateways.remove(gateway)
        else:
            merchant.gateways.add(gateway) 
    
    elif merchant_api and merchant_api.mtn_active == True and gateway and gateway.name == 'mtn_momo':
        merchant = request.merchant
        if gateway in merchant.gateways.all():
            merchant.gateways.remove(gateway)
        else:
            merchant.gateways.add(gateway)
    else:
        messages.error(request, f'{gateway.get_name_display()} must be created first!')
    
    gateways = PaymentGateway.objects.filter(status=True).exclude(name='balance')

    context = {
        'gateways': gateways,
    }
    return render(request, "merchants/partials/add_gateway.html", context)


@login_required
@user_is_merchant
def add_stripe_api(request):
    stripeform = StripeMerchantForm(request.POST or None, instance=request.merchant)
    if stripeform.is_valid():
        
        data = stripeform.cleaned_data

        stripeapi = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        stripeapi.stripe_public_key = data['stripe_public_key']
        stripeapi.stripe_secret_key = data['stripe_secret_key']
        stripeapi.stripe_webhook_key = data['stripe_webhook_key']
        stripeapi.stripe_subscription_price_id = data['stripe_subscription_price_id']
        stripeapi.sandbox = data['sandbox']
        stripeapi.stripe_active = True
        stripeapi.save()

    context = {
        'stripeform': stripeform,
    }
    return render(request, "merchants/partials/add_stripe_api.html", context)


@login_required
@user_is_merchant
def add_paypal_api(request):
    paypalform = PayPalMerchantForm(request.POST or None)
    
    if paypalform.is_valid():        
        data = paypalform.cleaned_data
        paypalapi = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        paypalapi.paypal_public_key = data['paypal_public_key']
        paypalapi.paypal_secret_key = data['paypal_secret_key']
        paypalapi.paypal_subscription_price_id = data['paypal_subscription_price_id']
        paypalapi.sandbox = data['sandbox']
        paypalapi.paypal_active = True
        paypalapi.save()

    context = {
        'paypalform': paypalform,
    }
    return render(request, "merchants/partials/add_paypal_api.html", context)


@login_required
@user_is_merchant
def add_flutterwave_api(request):
    flutterwaveform = FlutterwaveMerchantForm(request.POST or None)
    
    if flutterwaveform.is_valid():        
        data = flutterwaveform.cleaned_data
        flutterwaveapi = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        flutterwaveapi.flutterwave_public_key = data['flutterwave_public_key']
        flutterwaveapi.flutterwave_secret_key = data['flutterwave_secret_key']
        flutterwaveapi.flutterwave_subscription_price_id = data['flutterwave_subscription_price_id']
        flutterwaveapi.sandbox = data['sandbox']
        flutterwaveapi.flutterwave_active = True
        flutterwaveapi.save()
            
    context = {
        'flutterwaveform': flutterwaveform,
    }
    return render(request, "merchants/partials/add_flutterwave_api.html", context)


@login_required
@user_is_merchant
def add_razorpay_api(request):
    razorpayform = RazorpayMerchantForm(request.POST or None)
    
    if razorpayform.is_valid():        
        data = razorpayform.cleaned_data
        razorpayapi = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        razorpayapi.razorpay_public_key_id = data['razorpay_public_key_id']
        razorpayapi.razorpay_secret_key_id = data['razorpay_secret_key_id']
        razorpayapi.razorpay_subscription_price_id = data['razorpay_subscription_price_id']
        razorpayapi.sandbox = data['sandbox']
        razorpayapi.razorpay_active = True
        razorpayapi.save()

    context = {
        'razorpayform': razorpayform,
    }
    return render(request, "merchants/partials/add_razorpay_api.html", context)


@login_required
@user_is_merchant
def add_mtn_api(request):
    mtnform = MTNMerchantForm(request.POST or None)
    
    if mtnform.is_valid():        
        data = mtnform.cleaned_data
        mtnapi = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        mtnapi.mtn_api_user_id = data['mtn_api_user_id']
        mtnapi.mtn_api_key = data['mtn_api_key']
        mtnapi.mtn_subscription_key = data['mtn_subscription_key']
        mtnapi.mtn_callback_url = data['mtn_callback_url']
        mtnapi.sandbox = data['sandbox']
        mtnapi.mtn_active = True
        mtnapi.save()

    context = {
        'mtnform': mtnform,
    }
    return render(request, "merchants/partials/add_mtn_api.html", context)


























