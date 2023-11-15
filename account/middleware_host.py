from django.contrib.sites.models import Site
from django.http import HttpResponseNotFound
from django.conf import settings
from django.core.cache import cache
from general_settings.models import WebsiteSetting
from threadlocals.threadlocals import set_thread_variable
from account.models import Merchant


class DynamicHostMiddleware:
    """
    DynamicHostMiddleware
    ---------------------

    This middleware dynamically updates the ALLOWED_HOSTS setting based on 
    the domains stored in the Django Sites Framework database. 
    It ensures that incoming requests from allowed domains are processed 
    while requests from non-allowed domains receive an HttpResponseNotFound.

    - The allowed host list is cached in django to make retrieval effective
    - each time a domain is saved, this cache list become invalidated and
    - a new list is set with new request

    Usage:
    1. Add 'dynamic_host_middleware_app' to your Django project's settings.py MIDDLEWARE list.
    2. Ensure the Sites Framework is set up and the Site model is populated with allowed domains.

    Note:
    - This middleware requires the use of the Django Sites Framework.
    - Place it at the top of middleware to set the attributes.
    """
 
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.load_allowed_hosts()
        
        domain = request.get_host().lower().split(':')[0]
        if domain.startswith('www.'):
            domain = domain[4:]

        if domain not in settings.ALLOWED_HOSTS:
            return HttpResponseNotFound()
        
        try:
            site = Site.objects.select_related('websitesetting', 'merchant').get(domain=domain)
        except Site.DoesNotExist:
            site = Site.objects.select_related('websitesetting', 'merchant').get(pk=settings.SITE_ID)
        except Site.DoesNotExist:
            return HttpResponseNotFound()
        
        settings.SITE_ID = site.pk
        request.site = site
        # Set the request and current site in thread-local storage
        
        set_thread_variable('current_site', request.site)

        request.parent_site = None
        request.merchant = None

        if hasattr(site, 'websitesetting') and site.websitesetting:
            request.parent_site = site.websitesetting
            set_thread_variable('parent_site', request.parent_site.pk)
        elif hasattr(site, 'merchant') and site.merchant:
            request.merchant = site.merchant
            set_thread_variable('merchant', request.merchant.pk)

        # if WebsiteSetting.objects.filter(site=request.site).first():
        #     request.parent_site = request.site.websitesetting
        # else:
        #     request.merchant = Merchant.objects.filter(site=request.site).first()

        response = self.get_response(request)
        return response

    def load_allowed_hosts(self):
        cached_domains = cache.get('allowed_domains_cache')

        if cached_domains is None:
            site_domains = [site.domain for site in Site.objects.all()]
            cached_domains = list(set(site_domains) | set(settings.ALLOWED_HOSTS))
            cache.set('allowed_domains_cache', cached_domains, timeout=3600)
        settings.ALLOWED_HOSTS = cached_domains