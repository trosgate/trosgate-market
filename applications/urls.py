from django.urls import path
from . import views

app_name = 'applications'


urlpatterns = [
    # Urls for application addon table
    path('addon/', views.application_multiple_summary, name='application_multiple_summary'),
    path('addon-add/', views.add_application, name='add_application'),
    path('addon-remove/', views.remove_application, name='remove_application'),
    path('fees-structure/', views.application_fee_structure, name='application_fee_structure'),
    path('application-fee/', views.application_fee, name='application_fee'),

    # Urls for application table
    path('freelancer-application/', views.freelancer_application_view, name='freelancer_application'),
    path('client-application/', views.client_application_view, name='client_application'),
    path('<slug:project_slug>apply/', views.apply_for_project, name='apply_for_project'),
    path('applicants/<slug:project_slug>', views.application_detail, name='application_detail'),
    # Urls for Stripe gateway
    path('api/checkout/', views.final_application_checkout, name='final_application_checkout'),

    path('stripe/checkout/api/', views.stripe_application_intent, name='stripe_application_intent'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    # Urls for Paypal gateway
    path('paypal/checkout/api/', views.paypal_application_intent, name='paypal_payment_order'),
    path('success/', views.payment_success, name='hiring_payment_success'),
    path('congrats/', views.application_success, name='application_success'),

    path('flutter/checkout/api/', views.flutter_payment_intent, name='flutter_payment_intent'),
    path('razorpay/checkout/api/', views.razorpay_application_intent,name='razorpay_application_intent'),

    path('razorpay_webhook/', views.razorpay_webhook,name='razorpay_webhook'),
    #     path('payment_response/', views.payment_response, name='payment_response'),
]
