
from django.urls import path
from . import views

app_name = 'contract'

urlpatterns = [

    # Urls for contractor
    path('', views.add_contractor, name='contract_client'),

    # Urls for external contracts
    path('external/', views.external_contract_list, name='external_contract_list'),
    path('create/', views.create_external_contract, name='create_external_contract'),

    # Urls for internal contracts
    path('internal/', views.internal_contract_list, name='internal_contract_list'),
    path('accept_or_reject_contract', views.accept_or_reject_contract, name='accept_or_reject_contract'),
    path('contract_fee_selection/', views.contract_fee_selection, name='contract_fee_selection'),
    path('external_contract_fee_selection/', views.external_contract_fee_selection, name='external_contract_fee_selection'),

    # Urls for Paypal gateway
    path('paypal/checkout/api/', views.paypal_contract_intent, name='paypal_contract_intent'),
    path('external/paypal/checkout/', views.extern_paypal_contract_intent, name='extern_paypal_contract_intent'),
    # Urls for Stripe gateway
    path('stripe_contract_intent/', views.stripe_contract_intent, name='stripe_contract_intent'),
    path('extern_stripe_contract_intent/', views.extern_stripe_contract_intent, name='extern_stripe_contract_intent'),
    path('success/', views.payment_success, name='hiring_payment_success'),
    
    path('flutter_payment_intent/', views.flutter_payment_intent, name='flutter_payment_intent'),
    # Urls for Razorpay gateway
    path('razorpay_contract_intent/', views.razorpay_contract_intent, name='razorpay_contract_intent'),
    path('extern_razorpay_contract_intent/', views.extern_razorpay_contract_intent, name='extern_razorpay_contract_intent'),

    path('razorpay_webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    
    path('congrats/', views.contract_success, name='contract_success'),

    path('offer/<slug:short_name>/', views.create_internal_contract, name='create_internal_contract'),
    path('detail/<int:contract_id>/<slug:contract_slug>/', views.internal_contract_detail, name='internal_contract_detail'),
    path('intern/<int:contract_id>/<slug:contract_slug>/fees-structure/', views.internal_contract_fee_structure, name='internal_contract_fee_structure'),
    path('external/<int:contract_id>/<slug:contract_slug>/', views.external_contract_detail, name='external_contract_detail'),
    path('extern/<int:contract_id>/<slug:contract_slug>/fees-structure/', views.external_contract_fee_structure, name='external_contract_fee_structure'),
    path('checkout/<str:contract_id>/<slug:contract_slug>/', views.final_intcontract_checkout, name='final_contract_checkout'),
    path('externalcontract/<str:contract_id>/<slug:contract_slug>/', views.final_external_contract, name='final_external_contract'),
        
    # Urls for internal contracts chats   
    path('modify/<int:contractor_id>/', views.update_contractor, name='update_contractor'),
    path('delete/<int:contractor_id>/', views.delete_contractor, name='delete_contractor'),

]
htmx_urlpatterns = [
    path('discord/<int:contract_id>/<slug:contract_slug>/', views.contract_chat, name='contract_discord'),
    path('message/<int:contract_id>', views.create_contract_chat, name='create_contract_chat'),
    path('fetch/<int:contract_id>', views.fetch_messages, name='fetch_messages'),
]

urlpatterns += htmx_urlpatterns


