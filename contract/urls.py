
from django.urls import path
from . import views

app_name = 'contract'

urlpatterns = [

    # Urls for contractor
    path('', views.contract_list, name='contract_list'),
    path('add_contractor/', views.add_contractor, name='add_contractor'),
    path('connect/<str:reference>', views.create_external_contract, name='connect_contract'),
    path('delete/<str:contractor_id>', views.delete_contractor, name='delete_contractor'),
    path('offer/<slug:short_name>', views.create_internal_contract, name='create_internal_contract'),
    path('detail/<str:identifier>/<slug:contract_slug>', views.contract_detail, name='contract_detail'),
    path('gateway-and-fees/<str:identifier>/<slug:contract_slug>', views.pricing_option_with_fees, name='pricing_option_with_fees'),
    path('final/<str:identifier>/<slug:contract_slug>/checkout', views.final_contract_checkout, name='final_contract_checkout'),

    # Urls for Paypal gateway
    path('paypal/checkout/api/', views.paypal_contract_intent, name='paypal_contract_intent'),
    # path('paypal/external/', views.extern_paypal_contract_intent, name='extern_paypal_intent'),
    # Urls for Stripe gateway
    path('stripe_payment_intent/', views.stripe_payment_intent, name='stripe_payment_intent'),
    # path('extern_stripe_contract_intent/', views.extern_stripe_contract_intent, name='extern_stripe_contract_intent'),
    path('flutter-success/', views.flutter_contract_success, name='flutter_contract_success'),
    
    path('flutter_payment_intent/', views.flutter_payment_intent, name='flutter_payment_intent'),
    # Urls for Razorpay gateway
    path('razorpay_contract_intent/', views.razorpay_contract_intent, name='razorpay_contract_intent'),
    # path('extern_razorpay_contract_intent/', views.extern_razorpay_contract_intent, name='extern_razorpay_contract_intent'),
    # path('extern_razorpay/', views.extern_razorpay, name='extern_razorpay'),

    path('razorpay_webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    
    path('congrats/', views.contract_success, name='contract_success'),

        
]
htmx_urlpatterns = [
    path('accept_or_reject_contract', views.accept_or_reject_contract, name='accept_or_reject_contract'),
    path('refresh_contract/', views.refresh_contract, name='refresh_contract'),
    path('discord/<str:contract_id>/<slug:contract_slug>/', views.contract_chat, name='contract_discord'),
    path('message/<str:contract_id>', views.create_contract_chat, name='create_contract_chat'),
    path('fetch/<str:contract_id>', views.fetch_messages, name='fetch_messages'),
]

urlpatterns += htmx_urlpatterns


