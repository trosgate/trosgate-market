from django.http import HttpResponse
from .models import Customer, Merchant
from teams.models import Team
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import socket


class DomainValidator(RegexValidator):
    '''
    In this validator, we first use a regular expression 
    to check if the domain is in a valid format. 
    Then, we use the socket.getaddrinfo() method to attempt to resolve the DNS record for the domain. 
    If this fails, we raise a ValidationError indicating that the domain does not exist.
    '''
    regex = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$'
    message = _('Enter a valid domain name.')
    flags = 0

    def __call__(self, value):
        clean_domain = value.strip().lower()  # Clean the domain by removing any leading or trailing whitespace and lowercasing it
        super().__call__(clean_domain)
        try:
            # Check if the domain is available by attempting to resolve the DNS record for it
            socket.getaddrinfo(clean_domain, None)
        except socket.gaierror:
            raise ValidationError(_('The domain "%(clean_domain)s" does not exist.'), params={'value': clean_domain})


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
