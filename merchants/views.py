from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from general_settings.currency import get_base_currency_symbol
from account.models import Package, Merchant
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
    PaystackMerchantForm,
    FlutterwaveMerchantForm, 
    RazorpayMerchantForm, 
    CreditCardForm
)
from account.forms import (
    MerchantthemeForm,
    MerchantBrandingForm
)
from payments.checkout_card import CreditCard
from payments.checkout.paypal import PayPalClientConfig
from payments.checkout.stripe import StripeClientConfig
from payments.checkout.razorpay import RazorpayClientConfig
from payments.checkout.flutterwave import FlutterwaveClientConfig
from payments.checkout.paystack import PaystackClientConfig
from account.forms import DomainForm
from django.contrib.sites.models import Site



@login_required
@user_is_merchant
def theme_settings(request):
    themeform = MerchantthemeForm(request.POST or None, instance=request.merchant)
    brandingform = MerchantBrandingForm(request.POST or None, instance=request.merchant)
    context = {
        'themeform':themeform,
        'brandingform':brandingform,
    }

    return render(request, "merchants/theme.html", context)


@login_required
@user_is_merchant
def theme_form(request):
    themeform = MerchantthemeForm(request.POST, instance=request.merchant)
    if themeform.is_valid():
        themeform.save()
        messages.info(request, f'Saved successfully')
    context = {
        'themeform': themeform,
    }
    return render(request, "merchants/partials/theme.html", context)


@login_required
@user_is_merchant
def brand_form(request):
    brandingform = MerchantBrandingForm(request.POST, instance=request.merchant)
    if brandingform.is_valid():
        brandingform.save()
        messages.info(request, f'Saved successfully')
    context = {
        'brandingform': brandingform,
    }
    return render(request, "merchants/partials/brand.html", context)


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
                response = stripe_client.create_recurrent_test(
                    credit_card = data,
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
def domain_manager(request):
    context = {
        'domainform': DomainForm(),
    }

    return render(request, "merchants/domain_settings.html", context)


@login_required
@user_is_merchant
def update_domain(request):
    domainform = DomainForm(request.POST or None)

    if domainform.is_valid():
        domain = domainform.cleaned_data['domain']
        domain_lookup = Site.objects.filter(domain=domain)
        
        if domain_lookup.count():
            messages.error(request, f'Provided domain no longer available')
        else:
            merchant =request.user.merchant
            merchant.site.domain = domain
            merchant.site.save()
    else:
        messages.error(request, f'invalid domain input')

    context = {
        'domainform': DomainForm(),
    }

    return render(request, "merchants/partials/domain_settings.html", context)


@login_required
@user_is_merchant
def payment_settings(request):
    gateways = PaymentGateway.objects.filter(status=True).exclude(name='balance')
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    stripeform = StripeMerchantForm(request.POST or None, instance=merchant_api)
    paypalform = PayPalMerchantForm(request.POST or None, instance=merchant_api)
    flutterwaveform = FlutterwaveMerchantForm(request.POST or None, instance=merchant_api)
    paystackform = PaystackMerchantForm(request.POST or None, instance=merchant_api)
    razorpayform = RazorpayMerchantForm(request.POST or None, instance=merchant_api)
    context = {
        'merchant_api': merchant_api,
        'stripeform': stripeform,
        'paypalform': paypalform,
        'paystackform': paystackform,
        'flutterwaveform': flutterwaveform,
        'razorpayform': razorpayform,
        'gateways': gateways,
    }
    return render(request, "merchants/payment_settings.html", context)


@login_required
@user_is_merchant
def add_or_remove_gateway(request):
    gateway_pk = request.POST.get('mygateway')
    gateway = PaymentGateway.objects.filter(pk=gateway_pk, status=True).first()
    merchant_api = MerchantAPIs.objects.filter(merchant=request.merchant).first()

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
    
    elif merchant_api and merchant_api.flutterwave_active == True and gateway and gateway.name == 'paystack':
        merchant = request.merchant
        if gateway in merchant.gateways.all():
            merchant.gateways.remove(gateway)
        else:
            merchant.gateways.add(gateway)

    elif merchant_api and merchant_api.paystack_active == True and gateway and gateway.name == 'flutterwave':
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
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    stripeform = StripeMerchantForm(request.POST or None, instance=merchant_api)
    
    if stripeform.is_valid():
        stripeform.save()
        
        # data = stripeform.cleaned_data
        # merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        # merchant_api.stripe_public_key = data['stripe_public_key']
        # merchant_api.stripe_secret_key = data['stripe_secret_key']
        # merchant_api.stripe_webhook_key = data['stripe_webhook_key']
        # merchant_api.stripe_subscription_price_id = data['stripe_subscription_price_id']
        # merchant_api.stripe_active = True
        # merchant_api.save()

    context = {
        'merchant_api': merchant_api,
        'stripeform': stripeform,
        'paystackform' : PaystackMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_paypal_api(request):
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    paypalform = PayPalMerchantForm(request.POST or None, instance=merchant_api)
    
    if paypalform.is_valid():
        paypalform.save()

        # data = paypalform.cleaned_data

        # merchant_api.paypal_public_key = data['paypal_public_key']
        # merchant_api.paypal_secret_key = data['paypal_secret_key']
        # merchant_api.paypal_subscription_price_id = data['paypal_subscription_price_id']
        # merchant_api.sandbox = data['sandbox']
        # merchant_api.paypal_active = True
        # merchant_api.save()

    context = {
        'paypalform': paypalform,
        'paystackform' : PaystackMerchantForm(instance=merchant_api),
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_paystack_api(request):
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    paystackform = PaystackMerchantForm(request.POST or None, instance=merchant_api)

    if paystackform.is_valid():
        paystackform.save()
            
    context = {
        'paystackform': paystackform,
        'stripeform' : FlutterwaveMerchantForm(instance=merchant_api),
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_flutterwave_api(request):
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    flutterwaveform = FlutterwaveMerchantForm(request.POST or None, instance=request.merchant)
    # print(request.POST)
    if flutterwaveform.is_valid():
        flutterwaveform.save()

        # data = flutterwaveform.cleaned_data

        # merchant_api.flutterwave_public_key = data['flutterwave_public_key']
        # merchant_api.flutterwave_secret_key = data['flutterwave_secret_key']
        # merchant_api.flutterwave_subscription_price_id = data['flutterwave_subscription_price_id']
        # merchant_api.sandbox = data['sandbox']
        # merchant_api.flutterwave_active = True
        # merchant_api.save()
            
    context = {
        'flutterwaveform': flutterwaveform,
        'paystackform' : PaystackMerchantForm(instance=merchant_api),
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'razorpayform' : RazorpayMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)


@login_required
@user_is_merchant
def add_razorpay_api(request):
    merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
    razorpayform = RazorpayMerchantForm(request.POST or None, instance=merchant_api)
    
    if razorpayform.is_valid():
        razorpayform.save()
        # data = razorpayform.cleaned_data

        # merchant_api = MerchantAPIs.objects.get_or_create(merchant=request.merchant)[0]
        # merchant_api.razorpay_public_key_id = data['razorpay_public_key_id']
        # merchant_api.razorpay_secret_key_id = data['razorpay_secret_key_id']
        # merchant_api.razorpay_subscription_price_id = data['razorpay_subscription_price_id']
        # merchant_api.sandbox = data['sandbox']
        # merchant_api.razorpay_active = True
        # merchant_api.save()

    context = {
        'razorpayform': razorpayform,
        'paystackform' : PaystackMerchantForm(instance=merchant_api),
        'stripeform' : StripeMerchantForm(instance=merchant_api),
        'paypalform' : PayPalMerchantForm(instance=merchant_api),
        'flutterwaveform' : FlutterwaveMerchantForm(instance=merchant_api),
    }
    return render(request, "merchants/partials/create_payment.html", context)






















