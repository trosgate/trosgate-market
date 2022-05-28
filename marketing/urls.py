
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [

    # Urls for blog
    path('articles/', views.blog_list, name='blog_list'),
    path('articles/<slug:blog_slug>', views.blog_detail, name='blog_detail'),
    path('support/', views.support, name='support'),

]


