
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [

    # Urls for blog
    path('articles/', views.article_list, name='article_list'),
    path('articles/<slug:article_slug>', views.article_detail, name='article_detail'),
    path('support/', views.support, name='support'),

]


