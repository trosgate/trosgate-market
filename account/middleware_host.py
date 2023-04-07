# middleware.py

from django.contrib.sites.models import Site
from django.conf import settings
from account.models import Merchant
from django.http import HttpResponseForbidden


class DynamicHostMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # initialize and assign allowed host first before the check as we will use it
        settings.ALLOWED_HOSTS = self.load_allowed_hosts()

        domain = request.get_host().lower().split(':')[0]
        if domain.startswith('www.'):
            domain = domain[4:]

        if domain not in settings.ALLOWED_HOSTS:
            return HttpResponseForbidden()
        
        try:
            # Look up the Site object for the requested domain
            site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            return HttpResponseForbidden()

        # Set the SITE_ID header to the ID of the Site object
        request.site = site
        print (settings.ALLOWED_HOSTS)    
        if site.id == 1:
            request.parent_site = site
        else:
            request.parent_site = None

        request.tenant = self.is_merchant_family(request, site)

        response = self.get_response(request)    
        return response


    def load_allowed_hosts(self):
        site_domains = [site.domain for site in Site.objects.all()]
        return list(set(site_domains) | set(settings.ALLOWED_HOSTS))


    def is_merchant_family(self, request, site):
        """Check and assign object to Merchant."""

        if hasattr(request, 'user') and request.user.is_authenticated and not request.user.is_admin:
            print('goooooooooooooooooooooog goooooooooooooooog')
            return request.user.active_merchant_id
        else:
            return Merchant.objects.filter(site=site).first()

