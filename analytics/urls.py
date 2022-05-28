
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [

    # Urls for analytics app
    path('', views.time_tracker, name='time_tracker'),

]
