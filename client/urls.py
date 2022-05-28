from django.urls import path

from . import views

app_name = 'client'

# shared app urls
urlpatterns = [
    path('profile/<slug:short_name>/', views.client_profile, name='client_profile'),
    path('modify/<str:user_id>/', views.update_client, name='update_client_profile'),
    path('listing/', views.client_listing, name='client_listing'),
    path('deposit-fee/', views.deposit_fee_structure, name='deposit_fee_structure'),
    path('deposit_fee_session/', views.deposit_fee_session, name='deposit_fee_session'),
    path('deposit-final/', views.final_deposit, name='final_deposit'),
    path('stripe-deposit/', views.client_listing, name='client_listing'),
    path('congrats/', views.payment_success, name='payment_success'),
    
]
