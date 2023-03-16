from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from future.utilities import get_sms_feature
from django.contrib import messages
from django.apps import apps
from .forms import UserLoginForm


UserModel = apps.get_model('account', 'Customer')
# UserModel = settings.AUTH_USER_MODEL

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        current_site = get_current_site(request)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        
        if user.site == current_site:
            if user.check_password(password):
                return user
        return None


    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


    def user_type_redirect(self, request, user):
        session = request.session
        current_site = get_current_site(request)
        
        if user is not None and user.is_admin and user.site == current_site:
             
            login(request, user)

            messages.info(request, f'Welcome back {user.get_short_name()}')

            return redirect('/admin')

        # Checks for freelancer and redirect to 2FA or otherwise
        elif user is not None and user.is_freelancer and user.site == current_site and get_sms_feature():

            if "twofactoruser" not in session:
                session["twofactoruser"] = {"user_pk": user.pk}
                session.modified = True
                return redirect('account:two_factor_auth')

            return redirect('account:two_factor_auth')


        elif user is not None and user.is_freelancer and user.site == current_site and not get_sms_feature():
            
            login(request, user)

            messages.info(request, f'Welcome back {user.get_short_name()}')

            return redirect('account:dashboard')


        elif user is not None and user.is_client and user.site == current_site and get_sms_feature():

            if "twofactoruser" not in session:
                session["twofactoruser"] = {"user_pk": user.pk}
                session.modified = True
                return redirect('account:two_factor_auth')

            return redirect('account:two_factor_auth')


        elif user is not None and user.is_client and user.site == current_site and not get_sms_feature():            
            
            login(request, user)

            messages.info(request, f'Welcome back {user.get_short_name()}')

            return redirect('account:dashboard')
       
                                    
        elif user is not None and user.is_merchant and user.site == current_site and get_sms_feature():

            if "twofactoruser" not in session:
                session["twofactoruser"] = {"user_pk": user.pk}
                session.modified = True
                return redirect('account:two_factor_auth')

            return redirect('account:two_factor_auth')


        elif user is not None and user.is_merchant and user.site == current_site and not get_sms_feature():
            
            login(request, user)

            messages.info(request, f'Welcome back {user.get_short_name()}')

            return redirect('account:dashboard')

        elif user is not None and user.site != current_site:
            messages.info(request, f'Hi {user}, you are being redirected to {user.site.name} as you have account there')
            return redirect(f'http://{user.site.domain}:8000')
        
        else:
            messages.error(request, f'Invalid credentials')
            loginform = UserLoginForm()
            return render(request, "account/login.html", {'loginform': loginform})








































