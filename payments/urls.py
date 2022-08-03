
from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [

    # Urls for team table
    path('update_payment_account/', views.update_payment_account, name='update_payment_account'),
    path('<str:username>/', views.payment_modes, name='payment_modes'),
    path('transfers/', views.transfer_transactions, name='transfer_transactions'),
    path('withdrawals/', views.withdrawal_transactions, name='withdrawal_transactions'),
]
