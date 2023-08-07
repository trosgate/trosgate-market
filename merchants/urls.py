
from django.urls import path
from . import views


app_name = 'merchants'

urlpatterns = [

    # Urls for team table
    path('theme', views.theme_settings, name='theme_settings'),
    path('subscription', views.subscription, name='subscription'),
    path('subscribe-now/<str:type>', views.subscribe_now, name='subscribe_now'),
    path('payment-settings/', views.payment_settings, name='payment_settings'),
    path('domain-manager/', views.domain_manager, name='domain_manager'),

]


htmx_urlpatterns = [
    path('domains/', views.update_domain, name='update_domain'),
    path('subscribe_pay/', views.subscribe_pay, name='subscribe_pay'),
    path('add_or_remove_gateway/', views.add_or_remove_gateway, name='add_or_remove_gateway'),
    path('add_stripe_api/', views.add_stripe_api, name='add_stripe_api'),
    path('add_paypal_api/', views.add_paypal_api, name='add_paypal_api'),
    path('add_paystack_api/', views.add_paystack_api, name='add_paystack_api'),
    path('add_flutterwave_api/', views.add_flutterwave_api, name='add_flutterwave_api'),
    path('add_razorpay_api/', views.add_razorpay_api, name='add_razorpay_api'),
    path('add_mtn_api/', views.add_mtn_api, name='add_mtn_api'),
    path('stripe_subscription/', views.stripe_subscription, name='stripe_subscription'),

    path('theme_form/', views.theme_form, name='theme_form'),
    path('brand_form/', views.brand_form, name='brand_form'),
]

urlpatterns += htmx_urlpatterns
