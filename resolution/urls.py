
from django.urls import path
from . import views


app_name = 'resolution'

urlpatterns = [

    # Urls for team table
    path('<int:application_id>/<slug:project_slug>/',views.application_resolution, name='application_resolution'),

]
