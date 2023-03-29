
from django.urls import path
from . import views


app_name = 'merchants'

urlpatterns = [

    # Urls for team table
    path('payment-settings/', views.payment_settings, name='payment_settings'),

]


htmx_urlpatterns = [
    path('add_or_remove_gateway/', views.add_or_remove_gateway, name='add_or_remove_gateway'),
    path('add_stripe_api/', views.add_stripe_api, name='add_stripe_api'),
    path('add_paypal_api/', views.add_paypal_api, name='add_paypal_api'),
    path('add_flutterwave_api/', views.add_flutterwave_api, name='add_flutterwave_api'),
    path('add_razorpay_api/', views.add_razorpay_api, name='add_razorpay_api'),
    path('add_mtn_api/', views.add_mtn_api, name='add_mtn_api'),
]

urlpatterns += htmx_urlpatterns