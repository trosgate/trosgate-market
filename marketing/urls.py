
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [

    # Urls for blog
    path('notice', views.notice, name='notice'),
    path('articles', views.article_list, name='article_list'),
    path('support', views.ticket_and_support, name='support'),
    path('create-ticket', views.create_ticket, name='create_ticket'),
    path('ticket-list', views.customer_ticket_list, name='customer_ticket_list'),
    path('articles/<slug:article_slug>', views.article_detail, name='article_detail'),
    path('ticket/<str:reference>/<slug:ticket_slug>', views.customer_ticket_detail, name='customer_ticket_detail'),

]


