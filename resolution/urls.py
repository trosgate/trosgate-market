
from django.urls import path
from . import views


app_name = 'resolution'

urlpatterns = [

    # Urls for team table
    path('remove_message/',views.remove_message, name='remove_message'),
    path('applicant_start_work/',views.applicant_start_work, name='applicant_start_work'),
    path('applicant_review/',views.applicant_review, name='applicant_review'),
    path('app/<int:application_id>/<slug:project_slug>/',views.application_manager, name='application_resolution'),

    path('proposal_start_work/',views.proposal_start_work, name='proposal_start_work'),
    path('proposal_review/',views.proposal_review, name='proposal_review'),
    path('pro/<int:proposalsale_id>/<slug:proposal_slug>/',views.proposal_manager, name='proposal_resolution'),
    
    path('contract_start_work/',views.contract_start_work, name='contract_start_work'),
    path('contract_review/',views.contract_review, name='contract_review'),
    path('con/<int:contractsale_id>/<slug:contract_slug>/',views.contract_manager, name='contract_resolution'),
    
    path('oneclick_start_work/',views.oneclick_start_work, name='oneclick_start_work'),
    path('oneclick_review/',views.oneclick_review, name='oneclick_review'),
    path('one/<int:purchase_pk>/<str:reference>/',views.oneclick_manager, name='oneclick_manager'),
]
htmx_urlpatterns = [
    path('application_cancelled/', views.application_cancelled, name='application_cancelled'),
    path('confirm_application_cancel/', views.confirm_application_cancel, name='confirm_application_cancel'),
    path('proposal_cancelled/', views.proposal_cancelled, name='proposal_cancelled'),
    path('confirm_proposal_cancel/', views.confirm_proposal_cancel, name='confirm_proposal_cancel'),
    path('contract_cancelled/', views.internal_contract_cancelled, name='internal_contract_cancelled'),
    path('confirm_internal_contract/', views.confirm_internal_contract, name='confirm_internal_contract'),
    path('oneclick_cancelled/', views.oneclick_cancelled, name='oneclick_cancelled'),
    path('oneclick_confirm/', views.confirm_oneclick_contract, name='oneclick_confirm'),
]

urlpatterns += htmx_urlpatterns