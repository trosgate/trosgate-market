from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about-us', views.aboutus, name='aboutus'),
    path('terms-and-conditions', views.terms_and_conditions, name='terms_and_conditions'),
    path('how-it-works', views.how_it_works, name='how_it_works'),
    path('start_investment_now', views.start_investment_now, name='start_investment_now'),
]