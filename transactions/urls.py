from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [

    # Urls for hiring app
    # path('box-summary/', views.proposal_bucket,name='hiring_box_summary'),
    path('add/', views.add_proposal_to_box, name='add_to_hiring_box'),
    # path('pricing/', views.add_pricing_to_box, name='add_pricing_to_box'),
    path('remove/', views.remove_from_hiring_box, name='remove_from_hiring_box'),
    path('modify/', views.modify_from_hiring_box, name='modify_from_hiring_box'),

    #Transaction by type
    path('proposals/', views.proposal_transaction, name='proposal_transaction'),
    path('applications/', views.application_transaction, name='application_transaction'),
    path('contract/', views.contract_transaction, name='contract_transaction'),

    path('bucket-review/', views.pricing_option_with_fees, name='pricing_option_with_fees'),
    path('payment-fee-structure/', views.payment_fee_structure,name='payment_fee_structure'),
    path('checkout/', views.final_checkout, name='payment_checkout'),
    path('flutter_payment_intent/', views.flutter_payment_intent, name='flutter_payment_intent'),
    path('flutter_success/', views.flutter_success, name='flutter_success'),
    
    path('stripe_payment_intent/', views.stripe_payment_intent, name='stripe_payment_intent'),
    path('stripe_payment_order/', views.stripe_payment_order, name='stripe_payment_order'),
    path('paypal/api/', views.paypal_payment_order, name='paypal_payment_order'),
    path('paypal/callback/', views.paypal_callback, name='paypal_callback'),
    path('success/true/', views.payment_success, name='hiring_payment_success'),
    path('paystack_payment_intent/', views.paystack_payment_intent, name='paystack_payment_intent'),
    path('paystack_callback/', views.paystack_callback, name='paystack_callback'),
    path('razorpay_application_intent/', views.razorpay_application_intent,name='razorpay_application_intent'),
    path('razorpay_callback/', views.razorpay_callback,name='razorpay_callback'),    
    path('congrats/', views.payment_success, name='payment_success'),    
]
