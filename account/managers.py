from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from notification.mailer import new_user_registration
from django.db import transaction as db_transaction



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

        # try:
        #     db_transaction.on_commit(lambda: new_user_registration(user.pk))
        # except Exception as e:
        #     error = str(e)
        #     print(f"{error}")
        return user


    def create_staff(self, email, first_name, last_name, password=None, **extra_fields):
        curr_site = Site.objects.get_current()
        extra_fields.setdefault('site', curr_site)        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_superuser', False)
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
    
        with db_transaction.atomic():
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
            paymentapp = apps.get_model('payments', 'PaymentGateway') # This avoids circular import
            gateway = paymentapp.objects.get_or_create(name='balance')[0]
            
            domain = business_name.lower().replace(' ','-')
            curr_site = Site.objects.create(domain=f"{domain}.{site.domain}", name=f'{business_name}')
            merchant = merchantapp.objects.create(
                merchant=customer, 
                business_name=business_name, 
                site=curr_site, 
                packages=package,
                domain=f"{domain}.{site.domain}"
                )
            merchant.members.add(customer)
            merchant.gateways.add(gateway)

            customer.active_merchant_id = merchant.pk
            customer.save()

            teampackage = apps.get_model('teams', 'Package') 
            plans = ['basic', 'team']
            for plan in plans:
                teampackage.objects.create(merchant=merchant, type=plan)
                
            teampackage.objects.filter(merchant=merchant,type='team').update(
                max_proposals_allowable_per_team = merchant.packages.max_proposals_allowable_per_team,
                monthly_projects_applicable_per_team = merchant.packages.monthly_projects_applicable_per_team,
                monthly_offer_contracts_per_team = merchant.packages.monthly_offer_contracts_per_team,
                max_member_per_team = merchant.packages.max_member_per_team,
            )
        return customer
    

    def create_merchant_staff(self, email, password, first_name, last_name, merchant, **extra_fields):
        # Create merchant with the received information
        with db_transaction.atomic():
            merchantapp = apps.get_model('account', 'Merchant')
            curr_site = Site.objects.get_current()
            merchant = merchantapp.objects.filter(site=curr_site, merchant=merchant).first()

            if not merchant:
                raise ValueError(_('Something went wrong. Please try again'))
            
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_active', False)
            extra_fields.setdefault('is_superuser', False)
            extra_fields.setdefault('site', curr_site)
            extra_fields.setdefault('user_type', 'merchant')   
            
            customer = self.create_user(email, password, first_name=first_name, last_name=last_name, **extra_fields)
            customer.active_merchant_id = merchant.pk
            customer.save()
            
            merchant.members.add(customer)

        return customer
    

    def create_merchant_user(self, email, password, short_name, first_name, last_name, country, **extra_fields):
        # Create merchant with the received information
        with db_transaction.atomic():
            merchantapp = apps.get_model('account', 'Merchant')
            freelancerapp = apps.get_model('freelancer', 'Freelancer')
            freelanceraccountapp = apps.get_model('freelancer', 'FreelancerAccount')
            paymentapp = apps.get_model('payments', 'PaymentAccount')
            teamsapp = apps.get_model('teams', 'Team') 
            
            clientapp = apps.get_model('client', 'Client')
            packageapp = apps.get_model('teams', 'Package') 
            clientaccountapp = apps.get_model('client', 'ClientAccount')

            curr_site = Site.objects.get_current()
            merchant = get_object_or_404(merchantapp, site=curr_site)

            if not merchant:
                raise ValueError(_('Something went wrong. Please try again'))
            
            if not first_name:
                raise ValueError(_('Something went wrong. Please try again'))
            
            extra_fields.setdefault('site', curr_site)
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_active', False)
            extra_fields.setdefault('is_superuser', False)   
            
            if merchant and extra_fields.setdefault('user_type') == 'freelancer':
                extra_fields.setdefault('user_type', 'freelancer')
                
                user = self.create_user(email, password, short_name=short_name, first_name=first_name, last_name=last_name, country=country, **extra_fields)
                user.active_merchant_id = merchant.pk
                user.save()

                freelanceraccountapp.objects.get_or_create(merchant=merchant, user=user)[0]
                paymentapp.objects.get_or_create(merchant=merchant, user=user)[0]
                package = packageapp.objects.get_or_create(type='basic')[0]

                title = f'{user.short_name} Team'
                team = teamsapp.create_team_with_member(
                    title=title,
                    notice=f"This is the team for {user.short_name}", 
                    merchant=merchant,
                    created_by = user,
                    package=package,
                )
            
                freelancer = freelancerapp.objects.get_or_create(
                    merchant=merchant, 
                    user=user, active_team_id=team.id
                )[0]
                freelancer.active_team_id = team.id
                freelancer.save()

                return user

            if merchant and extra_fields.setdefault('user_type') == 'client':
                extra_fields.setdefault('user_type', 'client')
                user = self.create_user(email, password, short_name=short_name, first_name=first_name, last_name=last_name, country=country, **extra_fields)            
                user.active_merchant_id = merchant.pk
                user.save()
                            
                clientapp.objects.get_or_create(merchant=merchant, user=user)[0]
                clientaccountapp.objects.get_or_create(merchant=merchant, user=user)[0]

                return user
        
