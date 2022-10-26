
from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [

    # Urls for team table
    path('account-vault/', views.payment_vault, name='payment_vault'),
    path('transfers/', views.transfer_transactions, name='transfer_transactions'),
    path('withdrawals/', views.withdrawal_transactions, name='withdrawal_transactions'),
]
