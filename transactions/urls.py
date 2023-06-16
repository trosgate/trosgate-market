from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [

    # Urls for hiring app
    path('box-summary/', views.proposal_bucket,name='hiring_box_summary'),
    path('add/', views.add_proposal_to_box, name='add_to_hiring_box'),
    path('remove/', views.remove_from_hiring_box, name='remove_from_hiring_box'),
    path('modify/', views.modify_from_hiring_box, name='modify_from_hiring_box'),

    #Transaction by type
    path('proposals/', views.proposal_transaction, name='proposal_transaction'),
    path('applications/', views.application_transaction, name='application_transaction'),
    path('contract/', views.contract_transaction, name='contract_transaction'),

    path('fee-structure/', views.payment_option_with_fees, name='payment_option_selection'),
    path('payment_fee_structure/', views.payment_fee_structure,name='payment_fee_structure'),
    path('api/checkout/', views.final_checkout, name='payment_checkout'),
    path('flutter/checkout/api/', views.flutter_payment_intent, name='flutter_payment_intent'),
    # path('flutterwave_webhook/', views.flutterwave_webhook, name='flutterwave_webhook'),
    path('flutter_success/', views.flutter_success, name='flutter_success'),
    
    path('stripe/checkout/api/', views.stripe_payment_order, name='stripe_payment_order'),
    path('paypal/checkout/api/', views.paypal_payment_order, name='paypal_payment_order'),
    path('success/true/', views.payment_success, name='hiring_payment_success'),
    path('<str:short_name>/<slug:proposal_slug>', views.proposal_direct_hire, name='hiring_summary'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('razorpay/checkout/api/', views.razorpay_application_intent,name='razorpay_application_intent'),
    path('razorpay_webhook/', views.razorpay_webhook,name='razorpay_webhook'),    
    path('congrats/', views.payment_success, name='payment_success'),    
]
