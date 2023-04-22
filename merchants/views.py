from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import subprocess
import OpenSSL.crypto
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from general_settings.currency import get_base_currency_symbol
from account.models import Package
from freelancer.models import Freelancer, FreelancerAccount, FreelancerAction
from account.permission import user_is_merchant
from teams.forms import TeamCreationForm
from teams.models import Team, Invitation
from payments.models import (
    PaymentGateway, 
    MerchantAPIs,
    PaymentAccount, 
    PaymentRequest
)
from payments.forms import (
    StripeMerchantForm, 
    PayPalMerchantForm, 
    FlutterwaveMerchantForm, 
    RazorpayMerchantForm, 
    MTNMerchantForm,
    CreditCardForm
)

from payments.checkout_card import CreditCard
from payments.gateways.stripe import StripeClientConfig


@login_required
def subscription(request):
    merchant = request.merchant
    packages = Package.objects.all()
    context = {    
        'merchant': merchant,
        'packages': packages,
    }
    return render(request, "merchants/subscription.html", context)


@login_required
def subscribe_now(request, type):
    package = get_object_or_404(Package, type=type)
    session = request.session

    if "merchantpackage" not in session:
        session["merchantpackage"] = {"package_amount": package.price}
        session.modified = True
    else:
        session["merchantpackage"]["package_amount"] = package.price
        session.modified = True

    merchant = request.merchant
    gateways = PaymentGateway.objects.filter(status=True, subscription=True).exclude(name='balance')
    
    context = {    
        'merchant': merchant,
        'package': package,
        'gateways': gateways,
        'creditcardform': CreditCardForm(request=request),
    }
    return render(request, "merchants/subscribe_now.html", context)


@login_required
def subscribe_pay(request):
    amount = request.session["merchantpackage"]["package_amount"]
    merchant = request.merchant
    name = request.POST.get('mygateway')
    selectgateway = get_object_or_404(PaymentGateway, name=name)
    session = request.session

    if "merchantgateway" not in session:
        session["merchantgateway"] = {"gateway_id": selectgateway.name}
        session.modified = True
    else:
        session["merchantgateway"]["gateway_id"] = selectgateway.name
        session.modified = True

    gateways = PaymentGateway.objects.filter(status=True, subscription=True).exclude(name='balance')

    context = {    
        'amount': amount,
        'merchant': merchant,
        'gateways': gateways,
        'selectgateway': selectgateway,
        'creditcardform': CreditCardForm(request=request),
    }
    return render(request, "merchants/partials/subscribe_now.html", context)



@login_required
def stripe_subscription(request):
    amount = request.session["merchantpackage"]["package_amount"]
    gateway = request.session["merchantgateway"]["gateway_id"]
    merchant = request.merchant
    selectgateway = get_object_or_404(PaymentGateway, name=gateway)
    creditcardform = CreditCardForm(request.POST or None, request=request)
    stripe_client = StripeClientConfig(request)
    if request.method == "POST":
        if creditcardform.is_valid():
            credit_card = CreditCard(**creditcardform.cleaned_data)
            data = creditcardform.cleaned_data
            # print(data)
            try:
                response = stripe_client.create_recurrent(
                    credit_card = data,
                    package = 'Basic'
                )
            except Exception as e:
                print(str(e))
        else:
            messages.error(request, f'Invalid credential entered')    
    # number = request.POST.get("description", "")
    # verification_value = request.POST.get("customer_email", "")
    # success_url = request.POST.get("success_url", "")
    # cancel_url = request.POST.get("cancel_url", "")
    # amount = int(request.POST.get("amount", 0))
    # currency = "usd"
            

    gateways = PaymentGateway.objects.filter(status=True, subscription=True).exclude(name='balance')
    
    context = {    
        'merchant': merchant,
        'gateways': gateways,
        'amount': amount,
        'selectgateway': selectgateway,
        'creditcardform': creditcardform,
    }
    return render(request, "merchants/partials/subscribe_now.html", context)
    


@login_required
@user_is_merchant
def add_domain(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    value = request.POST.get('domain')
    domain = value.strip().lower()

    # Check if the domain already has an SSL certificate by looking for the certificate files in the /etc/letsencrypt/live directory
    cert_dir = os.path.join('/etc/letsencrypt/live', domain)
    cert_file = os.path.join(cert_dir, 'cert.pem')
    key_file = os.path.join(cert_dir, 'privkey.pem')
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        # If the certificate files already exist, do nothing
        return HttpResponse(f"{domain} already has an SSL certificate.")

    # Generate an SSL certificate using Certbot
    certbot_args = ['certonly', '--webroot', '-w', settings.WEBROOT_PATH, '-d', domain, '--non-interactive', '--agree-tos', '--email', request.user.email]
    try:
        subprocess.run(['certbot'] + certbot_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        return HttpResponseBadRequest(f"Failed to generate SSL certificate: {e.stderr}")

    # If the certificate was successfully generated, save the domain and keyfile path in the database
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        # Read the contents of the keyfile and save it to the database
        try:
            with open(key_file, 'rb') as f:
                keyfile_data = f.read()
        except IOError:
            return HttpResponseBadRequest("Failed to read keyfile.")

        # Save the domain and keyfile data to the database here...
        return HttpResponse(f"{domain} SSL certificate generated and saved.")
    else:
        # If the certificate files were not generated, return an error
        return HttpResponseBadRequest("Failed to generate SSL certificate.")


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

        merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        merchant_api.stripe_public_key = data['stripe_public_key']
        merchant_api.stripe_secret_key = data['stripe_secret_key']
        merchant_api.stripe_webhook_key = data['stripe_webhook_key']
        merchant_api.stripe_subscription_price_id = data['stripe_subscription_price_id']
        merchant_api.sandbox = data['sandbox']
        merchant_api.stripe_active = True
        merchant_api.save()

    context = {
        'merchant_api': merchant_api,
        'stripeform': stripeform,
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
        'mtnform' : MTNMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_paypal_api(request):
    paypalform = PayPalMerchantForm(request.POST or None, instance=request.merchant)
    
    if paypalform.is_valid():

        data = paypalform.cleaned_data

        merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        merchant_api.paypal_public_key = data['paypal_public_key']
        merchant_api.paypal_secret_key = data['paypal_secret_key']
        merchant_api.paypal_subscription_price_id = data['paypal_subscription_price_id']
        merchant_api.sandbox = data['sandbox']
        merchant_api.paypal_active = True
        merchant_api.save()

    context = {
        'paypalform': paypalform,
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
        'mtnform' : MTNMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_flutterwave_api(request):
    flutterwaveform = FlutterwaveMerchantForm(request.POST or None, instance=request.merchant)
    
    if flutterwaveform.is_valid():

        data = flutterwaveform.cleaned_data

        merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        merchant_api.flutterwave_public_key = data['flutterwave_public_key']
        merchant_api.flutterwave_secret_key = data['flutterwave_secret_key']
        merchant_api.flutterwave_subscription_price_id = data['flutterwave_subscription_price_id']
        merchant_api.sandbox = data['sandbox']
        merchant_api.flutterwave_active = True
        merchant_api.save()
            
    context = {
        'flutterwaveform': flutterwaveform,
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
        'mtnform' : MTNMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_razorpay_api(request):
    razorpayform = RazorpayMerchantForm(request.POST or None, instance=request.merchant)
    
    if razorpayform.is_valid():

        data = razorpayform.cleaned_data

        merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        merchant_api.razorpay_public_key_id = data['razorpay_public_key_id']
        merchant_api.razorpay_secret_key_id = data['razorpay_secret_key_id']
        merchant_api.razorpay_subscription_price_id = data['razorpay_subscription_price_id']
        merchant_api.sandbox = data['sandbox']
        merchant_api.razorpay_active = True
        merchant_api.save()

    context = {
        'razorpayform': razorpayform,
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),
        'mtnform' : MTNMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_mtn_api(request):
    mtnform = MTNMerchantForm(request.POST or None, instance=request.merchant)
    
    if mtnform.is_valid():

        data = mtnform.cleaned_data
        
        merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        merchant_api.mtn_api_user_id = data['mtn_api_user_id']
        merchant_api.mtn_api_key = data['mtn_api_key']
        merchant_api.mtn_subscription_key = data['mtn_subscription_key']
        merchant_api.mtn_callback_url = data['mtn_callback_url']
        merchant_api.sandbox = data['sandbox']
        merchant_api.mtn_active = True
        merchant_api.save()

    context = {
        'mtnform': mtnform,
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),        
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),    
    }
    return render(request, "merchants/partials/create_payment.html", context)

























