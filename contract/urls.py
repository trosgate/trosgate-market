
from django.urls import path
from . import views

app_name = 'contract'

urlpatterns = [

    # Urls for contractor
    path('', views.add_contractor, name='contract_client'),
    path('modify/<int:contractor_id>/', views.update_contractor, name='update_contractor'),
    path('delete/<int:contractor_id>/', views.delete_contractor, name='delete_contractor'),

    # Urls for external contracts
    path('external/', views.external_contract_list, name='external_contract_list'),
    path('create-external-contract/', views.create_external_contract, name='create_external_contract'),
    path('external/<int:contract_id>/<slug:urlcode>/', views.external_contract_detail, name='external_contract_detail'),
    path('payment/<slug:urlcode>/<slug:contract_slug>', views.redeem_external_contract, name='redeem_contract'),
    
    # Urls for internal contracts
    path('internal/', views.internal_contract_list, name='internal_contract_list'),
    path('accept_or_reject_contract', views.accept_or_reject_contract, name='accept_or_reject_contract'),
    path('contract_fee_selection/', views.contract_fee_selection, name='contract_fee_selection'),
    path('new/offer-to/<slug:short_name>/', views.create_internal_contract, name='create_internal_contract'),
    path('id/<int:contract_id>/<slug:contract_slug>/', views.internal_contract_detail, name='internal_contract_detail'),
    path('id/<int:contract_id>/<slug:contract_slug>/fees-structure/', views.internal_contract_fee_structure, name='internal_contract_fee_structure'),
    path('id/<int:contract_id>/<slug:contract_slug>/checkout/', views.final_contract_checkout, name='final_contract_checkout'),
    
    # Urls for internal contracts chats   
    path('discord/<int:contract_id>/<slug:contract_slug>/', views.contract_chat, name='contract_discord'),
    path('contract_chatroom/<int:contract_id>/', views.contract_chatroom, name='contract_chatroom'),

    # Urls for Stripe gateway
    path('stripe_contract_intent/', views.stripe_contract_intent, name='stripe_contract_intent'),
    # Urls for Paypal gateway
    path('paypal/<int:contract_id>/', views.paypal_contract_intent, name='paypal_contract_intent'),
    path('success/', views.payment_success, name='hiring_payment_success'),
    
    path('flutter_payment_intent/', views.flutter_payment_intent, name='flutter_payment_intent'),
    # Urls for Razorpay gateway
    path('razorpay_contract_intent/', views.razorpay_contract_intent, name='razorpay_contract_intent'),

    path('razorpay_webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    
    path('congrats/', views.contract_success, name='contract_success'),
]


