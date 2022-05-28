
from django.urls import path
from . import views

app_name = 'general_settings'


urlpatterns = [
   #Urls for category table 
    path('converter/', views.currency_conversion, name='converter'),      
    path('<slug:category_slug>/', views.category, name='category'),      

]
