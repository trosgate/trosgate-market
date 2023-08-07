
from django.urls import path
from . import views

app_name = 'proposals'


urlpatterns = [     
    #Urls users and teams
    path('', views.create_proposal, name='create_proposal'),
    path('list', views.proposal_listing, name='proposal_list'),
    path('proposal_filter/', views.proposal_filter, name='proposal_filter'),
    path('active-proposals/', views.active_proposal, name='active_proposal'),
    path('review-proposals/', views.review_proposal, name='review_proposal'),
    path('archived-proposals/', views.archive_proposal_page, name='archive_proposal_page'),
    path('archived/<str:short_name>/<slug:proposal_slug>', views.archive_proposal, name='archive_proposal'),
    path('restore/<str:short_name>/<slug:proposal_slug>', views.reactivate_archive_proposal, name='reactivate_archive_proposal'),
    path('detail/<str:short_name>/<slug:proposal_slug>', views.proposal_detail, name='proposal_detail'),
    path('preview/<str:short_name>/<slug:proposal_slug>', views.proposal_preview, name='proposal_preview'),

    # Proposal creation Steps
    path('introduction/', views.proposal_step_one, name='proposal_step_one'),
    path('background/', views.proposal_step_two, name='proposal_step_two'),
    path('faq/', views.proposal_step_three, name='proposal_step_three'),
    path('attribute/', views.proposal_step_four, name='proposal_step_four'),

    path('manage-proposal', views.merchant_proposal, name='merchant_proposal'),

    path('change/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposals, name='modify_proposals'),
    path('introduction/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_one, name='modify_proposal_step_one'),
    path('background/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_two, name='modify_proposal_step_two'),
    path('faq/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_three, name='modify_proposal_step_three'),
    path('attribute/<int:proposal_id>/<slug:proposal_slug>', views.modify_proposal_step_four, name='modify_proposal_step_four'),

    # Proposal chats   
    path('<slug:proposal_slug>/chat', views.proposal_chat_messages, name='proposal_chat_messages'),
    path('products/<str:proposal_ref>/', views.create_product_view, name='create_product_view'),
    path('attachment/<int:proposal_id>/', views.add_product_attachment, name='add_product_attachment'),
    path('download/<slug:proposal_slug>/<int:product_id>/', views.product_download, name='product_download'),
    path('themes-and-template/<slug:proposal_slug>/', views.product_detail, name='product_detail'),
   
]

htmx_urlpatterns = [
    path('message/<int:proposal_id>', views.create_message, name='create_message'),
    path('fetch_messages/<int:proposal_id>', views.fetch_messages, name='fetch_messages'),
    path('pricing', views.pricing_type, name='pricing_type'),
    path('modify/<slug:proposal_slug>/<int:product_id>/', views.product_update, name='product_update'),
    path('add/<int:proposal_id>/', views.add_products, name='add_products'),
]

urlpatterns += htmx_urlpatterns




