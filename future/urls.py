from django.urls import path
from . import views

app_name = 'plugins'


urlpatterns = [     
    #Urls users and teams
    path('', views.plugin_list, name='plugin_list'),
    path('<slug:plugin_slug>', views.plugin_detail, name='plugin_detail'),
]


htmx_urlpatterns = [
    # path('pricing', views.pricing_type, name='pricing_type'),
]

urlpatterns += htmx_urlpatterns
