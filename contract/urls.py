
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
    path('gateway-and-fees/<str:identifier>', views.pricing_option_with_fees, name='pricing_option_with_fees'),
    # path('payment-fee-structure/', views.payment_fee_structure,name='payment_fee_structure'),
    
    path('detail/<str:identifier>/<slug:contract_slug>', views.contract_detail, name='contract_detail'),
    path('final/<str:identifier>/<slug:contract_slug>/checkout', views.final_contract_checkout, name='final_contract_checkout'),

    # Urls for Stripe gateway
    path('stripe_payment_intent/', views.stripe_payment_intent, name='stripe_payment_intent'),
    path('stripe_payment_order/', views.stripe_payment_order, name='stripe_payment_order'),
    # Urls for Flutterwave gateway
    path('flutter_payment_intent/', views.flutter_payment_intent, name='flutter_payment_intent'),
    path('flutter_success/', views.flutter_success, name='flutter_success'),
    # Urls for Paypal gateway
    path('paypal/api/', views.paypal_payment_order, name='paypal_payment_order'),
    path('paypal/callback/', views.paypal_callback, name='paypal_callback'),
    # Urls for Paystack gateway
    path('paystack_payment_intent/', views.paystack_payment_intent, name='paystack_payment_intent'),
    path('paystack_callback/', views.paystack_callback, name='paystack_callback'),
    
    # Urls for Razorpay gateway
    path('razorpay_contract_intent/', views.razorpay_contract_intent, name='razorpay_contract_intent'),
    path('razorpay_callback/', views.razorpay_callback, name='razorpay_callback'),
    
]
htmx_urlpatterns = [
    path('accept_or_reject_contract', views.accept_or_reject_contract, name='accept_or_reject_contract'),
    path('refresh_contract/', views.refresh_contract, name='refresh_contract'),
    path('discord/<str:contract_id>/<slug:contract_slug>/', views.contract_chat, name='contract_discord'),
    path('message/<str:contract_id>', views.create_contract_chat, name='create_contract_chat'),
    path('fetch/<str:contract_id>', views.fetch_messages, name='fetch_messages'),
]

urlpatterns += htmx_urlpatterns


