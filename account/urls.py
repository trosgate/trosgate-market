from django.urls import path
from django.contrib.auth import views as auth_views
from .views import account_register, account_activate, homepage
from .forms import PasswordResetForm, PasswordResetConfirmForm
from django.views.generic import TemplateView
from . import views
from . validators import verify_username, verify_team, user_types
from general_settings.utilities import (
    website_name,
    get_protocol_with_domain_path,
)

app_name = 'account'

# shared accounts app urls
urlpatterns = [
    # path('countries/', views.countries, name='countries'),
    # path('states/', views.states, name='states'),

    path('', views.homepage, name='homepage'),
    path("account/login/", views.loginView, name = "login"),
    path('dashboard/', views.user_dashboard, name='dashboard'), 
    path("account/two-factor-auth/", views.two_factor_auth, name = "two_factor_auth"),    
    path("logout/", views.Logout, name="logout"),
    path("autologout/", views.autoLogout, name="autologout"),
    path('account/register/', account_register, name='register'),
    path("activate/<slug:uidb64>/<slug:token>)/", account_activate, name="activate"),
  
    # User Reset password
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="account/user/password_reset_form.html",
        success_url="password_reset_email_confirm",
        email_template_name="account/user/password_reset_email.html",
        extra_context = {'protocol_with_domain_path':get_protocol_with_domain_path(), 'website_name':website_name()},
        form_class=PasswordResetForm,
    ),
        name="passwordreset",
    ),
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(
        template_name="account/user/password_reset_confirm.html",
        success_url="/password_reset_complete/",
        extra_context = {'protocol_with_domain_path':get_protocol_with_domain_path(), 'website_name':website_name()},        
        form_class=PasswordResetConfirmForm,
    ),
        name="password_reset_confirm",
    ),
    path("password_reset/password_reset_email_confirm/", TemplateView.as_view(
        template_name="account/user/reset_status.html"),
        name="password_reset_done",
    ),
    path("password_reset_complete/", TemplateView.as_view(
        template_name="account/user/reset_status.html"),
        name="password_reset_complete",
    ),
        
]

htmx_urlpatterns = [
    path("verify_username/", verify_username, name = "verify_username"), 
    path("verify_team/", verify_team, name = "verify_team"),
    path('user_types/', user_types, name='user_types'),
]

urlpatterns += htmx_urlpatterns
