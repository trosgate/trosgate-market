
from django.urls import path
from . import views


app_name = 'resolution'

urlpatterns = [

    # Urls for team table
    path('applicant_start_work/',views.applicant_start_work, name='applicant_start_work'),
    path('applicant_review/',views.applicant_review, name='applicant_review'),
    path('app/<str:application_id>/<slug:project_slug>/',views.application_resolution, name='application_resolution'),

    path('proposal_start_work/',views.proposal_start_work, name='proposal_start_work'),
    path('proposal_review/',views.proposal_review, name='proposal_review'),
    path('pro/<str:proposal_id>/<slug:proposal_slug>/',views.proposal_resolution, name='proposal_resolution'),
]
