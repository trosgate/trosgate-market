
from django.urls import path
from . import views

# IMPORT SUBSCRIPTIONS
from .stripe_subscription import stripe_subscription_checkout_session
from .razorpay_subscription import razorpay_subscription_checkout_session, razorpay_subscription_webhook
from .paypal_subscription import activate_paypal_subscription, deactivate_paypal_subscription


app_name = 'teams'

urlpatterns = [
    path('', views.team, name='team'),
    path('send-test-email', views.send_email_to_all_users, name='send_email_to_all_users'),
    path('change_shareholding', views.change_shareholding, name='change_shareholding'),

    # payment subscription urls
    path('packages/', views.packages, name='packages'),
    path('subscription/', views.purchase_package, name='purchase_package'),
    path('packages/success/', views.package_success, name='package_success'),
    path('packages/paypal/create/', views.paypal_package_order, name='paypal_package_order'),
    # Urls for team table
    path('message/', views.teamchat, name='teamchat'),
    path('chat/', views.teamchatroom, name='teamchatroom'),
    path('accept/', views.accept_team_invitation, name='accept_invite'),
    path('assigned/to/me/', views.assign_proposals_to_me, name='assign_to_me'),
    path('assigned/to/members/', views.assigned_proposals_to_members, name='assign_to_members'),

    # payment api with stripe urls
    path('stripe_subscription_checkout_session/', stripe_subscription_checkout_session, name='stripe_subscription_checkout_session'),
    path('razorpay_subscription_checkout_session/', razorpay_subscription_checkout_session, name='razorpay_subscription_checkout_session'),
    path('razorpay_subscription_webhook/', razorpay_subscription_webhook, name='razorpay_subscription_webhook'),

    # payment api with paypal urls
    path('activate_paypal_subscription/', activate_paypal_subscription, name='activate_paypal_subscription'),
    path('deactivate_paypal_subscription/', deactivate_paypal_subscription, name='deactivate_paypal_subscription'),

    path('reassign/<int:assign_id>/<slug:proposal_slug>/', views.re_assign_proposal_to_any_member, name='re_assign_proposal_to_any_member'),
    path('myself/<int:member_id>/', views.reassign_proposals_to_myself, name='reassign_proposals_to_myself'),
    path('invitation/', views.invitation, name='invitation'),
    path('activate/<int:team_id>/', views.activate_team, name='activate_team'),
    path('preview/<int:team_id>/', views.preview_team, name='preview_inactive_team'),
    path('detail/', views.team_single, name='team_single'),
    path('internal_invitation/', views.internal_invitation, name='internal_invitation'),
    path('external_invitation/', views.external_invitation, name='external_invitation'),
    
    path('assign/<slug:team_slug>/<slug:proposal_slug>/',views.assign_proposal, name='assign_proposal'),
    path('tracker/<slug:proposal_slug>/<int:assign_id>/',views.proposal_tracking, name='proposal_tracking'),
    path('modify/<slug:proposal_slug>/<int:assign_id>/<int:tracking_id>/',views.modify_proposal_tracking, name='modify_proposal_tracking'),
    path('delete/<slug:proposal_slug>/<int:assign_id>/<int:tracking_id>/',views.delete_proposal_tracking, name='delete_proposal_tracking'),


]
htmx_urlpatterns = [
    path('update/', views.update_team, name='update_team'),
    path('remove-invitee/', views.remove_invitee, name='remove_invitee'), 
    path('gallery/', views.team_gallery, name='team_gallery'), 
]

urlpatterns += htmx_urlpatterns