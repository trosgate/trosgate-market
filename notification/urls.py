from django.urls import path, re_path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.notifications, name='notifications'),
]