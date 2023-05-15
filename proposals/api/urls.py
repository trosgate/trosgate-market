from django.urls import path
from proposals.api import views

app_name = 'proposal_api'


urlpatterns = [     
    #Urls users and teams
    # path('', views.api_proposal_detail, name='api_proposal_detail'),
    path('detail/<str:short_name>/<slug:proposal_slug>', views.api_proposal_detail, name='api_proposal_detail'),
    path('change/<int:proposal_id>/<slug:api_proposal_update>', views.api_proposal_update, name='api_proposal_update'),
]