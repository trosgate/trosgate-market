
from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [

    # Urls for team table
    path('account-vault/', views.payment_vault, name='payment_vault'),
    path('transfers/', views.transfer_transactions, name='transfer_transactions'),
    path('withdrawals/', views.withdrawal_transactions, name='withdrawal_transactions'),
    path('packages/paypal/create/', views.paypal_package_order, name='paypal_package_order'),
    path('subscriptions', views.package_transaction, name='package_transaction'),
]

htmx_urlpatterns = [
    path('balance/', views.subscribe_with_balance, name='subscribe_with_balance'),

]

urlpatterns += htmx_urlpatterns