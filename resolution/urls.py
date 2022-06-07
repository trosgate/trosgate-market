
from django.urls import path
from . import views


app_name = 'resolution'

urlpatterns = [

    # Urls for team table
    path('applicant_start_work/',views.applicant_start_work, name='applicant_start_work'),
    path('applicant_review/',views.applicant_review, name='applicant_review'),
    path('<int:application_id>/<slug:project_slug>/',views.application_resolution, name='application_resolution'),

]
