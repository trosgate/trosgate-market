from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps



class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError(_("The given email field is required"))
        if not first_name:
            raise ValueError(_("Usernam field is required"))
        if not last_name:
            raise ValueError(_("Usernam field is required"))
        if not password:
            raise ValueError(_("You must set a valid password"))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_staff(self, email, first_name, last_name, password=None, **extra_fields):
        curr_site = Site.objects.get_current()
        extra_fields.setdefault('site', curr_site)        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_superuser', False)
        curr_site = Site.objects.get_current()
        return self.create_user(email, first_name=first_name, last_name=last_name, password=password, **extra_fields)


    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        curr_site = Site.objects.get_current()
        extra_fields.setdefault('site', curr_site)        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have Allow Login Access'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email=email, password=password, first_name=first_name, last_name=last_name, **extra_fields)


    def create_merchant(self, email, password, first_name, last_name, business_name, country, package, **extra_fields):
        if not package:
            raise ValueError(_('Unknown package selected')) 
        
        site = Site.objects.get_current()
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('site', site)
        extra_fields.setdefault('user_type', 'merchant')

        customer = self.create_user(email, password, first_name=first_name, last_name=last_name, country=country, **extra_fields)
        
        # Create merchant with the received information
        merchantapp = apps.get_model('account', 'Merchant') # This avoids circular import
        
        domain = business_name.lower().replace(' ','-')
        curr_site = Site.objects.create(domain=f"{domain}.{site.domain}", name=f'{business_name}')
        merchantapp.objects.create(merchant=customer, business_name=business_name, site=curr_site, package=package)
        
        return customer
    

    def create_freelancer(self, email, team, password=None, **extra_fields):
        if not package:
            raise ValueError(_('Unknown package selected'))
         
        team_instance = Team.objects.create(name=f"{email}'s team'")
        extra_fields.setdefault('team', team_instance)
        extra_fields.setdefault('is_freelancer', True)
        
        site = Site.objects.get_current()
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('site', site)
        extra_fields.setdefault('user_type', 'merchant')


        return

