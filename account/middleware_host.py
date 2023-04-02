# middleware.py
import re
from django.contrib.sites.models import Site
from django.conf import settings
from account.models import Merchant
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse


class DynamicHostMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.get_host().lower().split(':')[0]
        if domain.startswith('www.'):
            domain = domain[4:]

        try:
            # Look up the Site object for the requested domain
            site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            return HttpResponseForbidden()

        # Configure the upstream server based on the value of the HTTP_UPSTREAM header
        settings.ALLOWED_HOSTS = [str(site), site.name, site.domain]
        # Set an attribute to differentiate parent site instance from all other merchants
        
        # Set the SITE_ID header to the ID of the Site object
        request.site = site.id
            
        if site.id == 1:
            request.parent_site = site
        else:
            request.parent_site = None

        request.tenant = self.is_merchant_family(request, site)
        response = self.get_response(request)    
        return response


    def is_merchant_family(self, request, site):
        """Check and assign object to Merchant."""
        if not request.user.is_authenticated:
            return Merchant.objects.filter(site=site).first()
        elif request.user.is_authenticated and not request.user.is_admin:
            return request.user.active_merchant_id
        
