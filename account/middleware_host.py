from django.contrib.sites.models import Site
from django.conf import settings
from account.models import Merchant
from django.http import HttpResponseForbidden, HttpResponseNotFound




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
            return HttpResponseNotFound()
        
        try:
            # Look up the Site object for the requested domain
            site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            return HttpResponseForbidden()

        # Set the SITE_ID header to the ID of the Site object
        settings.SITE_ID = site.id 
        request.site = site

        request.merchant = None
        request.parent_site = None

        if request.site.domain == settings.SITE_DOMAIN:
            request.parent_site = site
                   
        if request.site.domain != settings.SITE_DOMAIN:
            request.merchant = site
            # request.merchant = self.is_merchant_family(request)
        
        response = self.get_response(request)
        return response


    def load_allowed_hosts(self):
        site_domains = [site.domain for site in Site.objects.all()]
        return list(set(site_domains) | set(settings.ALLOWED_HOSTS))


    def is_merchant_family(self, request):
        """Check and assign object to Merchant."""

        return Merchant.objects.filter(site=request.site).first()
        