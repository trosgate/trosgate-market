from django.urls import path

from . import views

app_name = 'freelancer'

# shared app urls
urlpatterns = [
    path('transfer-or-withdraw/', views.transfer_or_withdraw, name='transfer_or_withdraw'),
    path('transfer_debit/', views.transfer_debit, name='transfer_debit'),
    path('withdrawal_debit/', views.withdrawal_debit, name='withdrawal_debit'),
    path('profile/<slug:short_name>/', views.freelancer_profile, name='freelancer_profile'),
    path('modify/<str:short_name>', views.update_freelancer, name='update_freelancer_profile'),
    path('listing/', views.freelancer_listing, name='freelancer_listing'),    
    path('freelancer_search/', views.freelancer_search, name='freelancer_search'),    
]

