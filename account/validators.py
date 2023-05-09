from django.http import HttpResponse
from .models import Customer, Merchant
from teams.models import Team
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.forms import CharField
from django.core.validators import RegexValidator
import socket


DOMAIN_NAME_REGEX = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$'

class DomainField(CharField):
    '''
    In this validator, we first use a regular expression 
    to check if the domain is in a valid format.
    '''
    default_validators = [RegexValidator(DOMAIN_NAME_REGEX, 'Enter a valid domain name.')]


class DomainValidator:
    ''' 
    Then, we use the socket.getaddrinfo() method to attempt to 
    resolve the DNS record for the domain. 
    If this fails, we raise a ValidationError indicating 
    that the domain does not exist.
    '''
    def __init__(self, domain):
        self.domain = domain

    def validate(self):
        try:
            # Try to resolve the domain name
            socket.getaddrinfo(self.domain, None)
        except socket.gaierror:
            # An error occurred, which means the domain is invalid or doesn't exist
            return False
        else:
            # The domain exists and is valid
            return True


def verify_username(request):
    short_name = request.POST.get('short_name')
    if len(short_name) < 4:
        return HttpResponse("<div style='color:red;'> The username must be four characters or more </div>")
    else:
        if Customer.objects.filter(short_name=short_name).exists():
            return HttpResponse("<div id='short_name-status' class='shortnameerrors' style='color:red;'> Username already taken </div>")
        else:
            return HttpResponse("<div id='short_name-status' class='shortnamesuccess' style='color:green;'> This username is available </div>") 


def verify_team(request):
    title = request.POST.get('title')
    if Team.objects.filter(title=title).exists():
        return HttpResponse("<div style='color:red;'> This name already taken </div>")
    else:
        return HttpResponse("<div style='color:green;'> This name is available </div>") 


def user_types(request):
    type = request.GET.get('user_type')
    if type =="freelancer":
        return HttpResponse("<div style='color:blue;'>Info: A freelancer will work and get paid</div>")
    else:
        return HttpResponse("<div style='color:blue;'>Info: A client will create jobs and employ</div>")


def build_subdomain(request):
    business_name = request.POST.get('business_name')
    site = Site.objects.get_current()
    domain = business_name.lower().replace(' ','-')
    full_domain = f"{domain}.{site.domain}"

    registered = Merchant.objects.filter(business_name__iexact=business_name)
    
    if business_name and registered.count():
        return HttpResponse(f"<div id='business_name_status' style='color:red;' class='wt-tabscontenttitle'> Your business name already exists. Login instead</div>")
    
    elif business_name and not registered.count():
        return HttpResponse(f"<div id='business_name_status' style='color:green;' class='wt-tabscontenttitle'> Your domain will be: {full_domain} but you can later change</div>")
   
    else:
        return HttpResponse(" ")
