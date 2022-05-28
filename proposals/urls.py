
from django.urls import path
from . import views

app_name = 'proposals'


urlpatterns = [     
    #Urls for proposals table
    path('', views.proposal_list, name='proposal_list'),
    path('active-proposals/', views.active_proposal, name='active_proposal'),
    path('create-proposal/', views.create_proposal, name='create_proposal'),
    path('review-proposals/', views.review_proposal, name='review_proposal'),
    path('archived-proposals/', views.archive_proposal_page, name='archive_proposal_page'),
    path('archived<str:short_name>/<slug:proposal_slug>', views.archive_proposal, name='archive_proposal'),
    path('restore/<str:short_name>/<slug:proposal_slug>', views.reactivate_archive_proposal, name='reactivate_archive_proposal'),
    # path('modify/<slug:proposal_slug>/', views.modify_proposal, name='modify_proposal'),
    path('<str:short_name>/<slug:proposal_slug>', views.proposal_detail, name='proposal_detail'),
    path('modify/<str:short_name>/<slug:proposal_slug>', views.update_proposal, name='update_proposal'),

    # path('invoice/client', views.create_invoice_client, name='invoice_client'),
    path('create-invoice/', views.add_invoice, name='create_invoice'),
   
]
