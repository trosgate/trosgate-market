
from django.urls import path
from . import views

app_name = 'proposals'


urlpatterns = [     
    #Urls for proposals table
    path('', views.proposal_list, name='proposal_list'),
    path('active-proposals/', views.active_proposal, name='active_proposal'),
    path('review-proposals/', views.review_proposal, name='review_proposal'),
    path('archived-proposals/', views.archive_proposal_page, name='archive_proposal_page'),
    path('archived<str:short_name>/<slug:proposal_slug>', views.archive_proposal, name='archive_proposal'),
    path('restore/<str:short_name>/<slug:proposal_slug>', views.reactivate_archive_proposal, name='reactivate_archive_proposal'),
    path('<str:short_name>/<slug:proposal_slug>', views.proposal_detail, name='proposal_detail'),
    path('preview/<str:short_name>/<slug:proposal_slug>', views.proposal_preview, name='proposal_preview'),

    # Proposal creation Steps
    path('introduction/', views.proposal_step_one, name='proposal_step_one'),
    path('background/', views.proposal_step_two, name='proposal_step_two'),
    path('faq/', views.proposal_step_three, name='proposal_step_three'),
    path('attribute/', views.proposal_step_four, name='proposal_step_four'),

    path('introduction/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_one, name='modify_proposal_step_one'),
    path('background/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_two, name='modify_proposal_step_two'),
    path('faq/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_three, name='modify_proposal_step_three'),
    path('attribute/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_four, name='modify_proposal_step_four'),

    # Proposal chats   
    path('chats/', views.proposal_chat_messages, name='proposal_chat_messages'),

   
]
