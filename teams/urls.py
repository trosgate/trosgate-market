
from django.urls import path
from . import views

# , stripe_webhook
from .stripe_subscription import stripe_subscription_checkout_session
from .razorpay_subscription import razorpay_subscription_checkout_session, razorpay_subscription_callback

app_name = 'teams'

urlpatterns = [

    # Urls for team table
    path('', views.team, name='team'),
    path('message/', views.teamchat, name='teamchat'),
    path('chat/', views.teamchatroom, name='teamchatroom'),
    path('email/', views.send_email_to_all_users, name='email_freelancer'),
    path('schedule/', views.Admin_email_scheduler, name='email_schedule'),
    path('accept/', views.accept_team_invitation, name='accept_invite'),
    path('assigned/to/me/', views.assign_proposals_to_me, name='assign_to_me'),
    path('assigned/to/members/', views.assigned_proposals_to_members,
         name='assign_to_members'),
    path('reassigned/<int:assign_id>/<slug:proposal_slug>/',
         views.re_assign_proposal_to_any_member, name='re_assign_proposal_to_any_member'),
    path('reassigned/<int:member_id>/', views.reassign_proposals_to_myself,
         name='reassign_proposals_to_myself'),
    path('invitation/', views.invitation, name='invitation'),
    path('update/<int:team_id>/', views.update_teams, name='update_team'),
    path('activate/<int:team_id>/', views.activate_team, name='activate_team'),
    path('preview/<int:team_id>/', views.preview_team,
         name='preview_inactive_team'),
    path('delete/<int:team_id>/', views.delete_teams, name='delete_team'),
    path('detail/<int:team_id>/', views.team_single, name='team_single'),
    path('internal-user/<slug:short_name>/',
         views.internal_invitation, name='internal_invitation'),
    path('assign/<slug:team_slug>/<slug:proposal_slug>/',
         views.assign_proposal, name='assign_proposal'),
    path('tracker/<slug:proposal_slug>/<int:assign_id>/',
         views.proposal_tracking, name='proposal_tracking'),
    path('modify/<slug:proposal_slug>/<int:assign_id>/<int:tracking_id>/',
         views.modify_proposal_tracking, name='modify_proposal_tracking'),
    path('delete/<slug:proposal_slug>/<int:assign_id>/<int:tracking_id>/',
         views.delete_proposal_tracking, name='delete_proposal_tracking'),

    # payment subscription urls
    path('packages/', views.packages, name='packages'),
    path('package/<slug:type>/', views.purchase_package, name='purchase_package'),
    path('packages/success/', views.plans_activated, name='package_success'),
    path('packages/paypal/create/', views.paypal_package_order, name='paypal_package_order'),

    # payment api with stripe urls
    path('api/stripe_subscription_checkout_session/', stripe_subscription_checkout_session, name='stripe_subscription_checkout_session'),
    path('razorpay_subscription_checkout_session/', razorpay_subscription_checkout_session, name='razorpay_subscription_checkout_session'),
    path('razorpay_subscription_callback/', razorpay_subscription_callback, name='razorpay_subscription_callback'),

]
