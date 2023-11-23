
from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [

    # Urls for team table
    path('account-vault/', views.payment_vault, name='payment_vault'),
    path('transfers/', views.transfer_transactions, name='transfer_transactions'),
    path('withdrawals/', views.withdrawal_transactions, name='withdrawal_transactions'),
    path('subscriptions', views.package_transaction, name='package_transaction'),
]

htmx_urlpatterns = [
    path('balance/', views.subscribe_with_balance, name='subscribe_with_balance'),
    path('subscribe_with_stripe/', views.subscribe_with_stripe, name='subscribe_with_stripe'),
    path('stripe_confirmation/', views.stripe_confirmation, name='stripe_confirmation'),
    path('paypal_subscription/', views.paypal_subscription, name='paypal_subscription'),

]

urlpatterns += htmx_urlpatterns