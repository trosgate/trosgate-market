from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Urls for application addon table
    path('gateway-and-fees', views.pricing_option_with_fees, name='pricing_option_with_fees'),
    path('select-applicant/', views.add_or_remove_application, name='add_or_remove_application'),
    path('addon-remove/', views.remove_application, name='remove_application'),
    # path('application-fee/', views.application_fee, name='application_fee'),

    # Urls for application table
    path('freelancer-application/', views.freelancer_application_view, name='freelancer_application'),
    path('client-application/', views.client_application_view, name='client_application'),
    path('<slug:project_slug>/apply/', views.apply_for_project, name='apply_for_project'),
    path('applicants/<slug:project_slug>', views.application_detail, name='application_detail'),
    # Urls for Stripe gateway
    path('api/checkout/', views.final_application_checkout, name='final_application_checkout'),

    path('paystack_payment_intent/', views.paystack_payment_intent, name='paystack_payment_intent'),
    path('paystack_callback/', views.paystack_callback, name='paystack_callback'),
    path('razorpay_application_intent/', views.razorpay_application_intent,name='razorpay_application_intent'),
    path('razorpay_callback/', views.razorpay_callback,name='razorpay_callback'),    

    path('flutter_payment_intent/', views.flutter_payment_intent, name='flutter_payment_intent'),
    path('flutter_success/', views.flutter_success, name='flutter_success'),
    
    path('stripe_payment_intent/', views.stripe_payment_intent, name='stripe_payment_intent'),
    path('stripe_payment_order/', views.stripe_payment_order, name='stripe_payment_order'),
    path('paypal/api/', views.paypal_payment_order, name='paypal_payment_order'),
    path('paypal/callback/', views.paypal_callback, name='paypal_callback'),
]
