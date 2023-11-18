from django.http import HttpResponseNotFound
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.cache import cache
from threadlocals.threadlocals import set_thread_variable
from django.db.models import Q



class DynamicHostMiddleware:
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
            return HttpResponseNotFound()

        settings.SITE_ID = site.pk
        request.site = site
        set_thread_variable('current_site', request.site)

        request.parent_site = getattr(site, 'websitesetting', None)
        request.merchant = getattr(site, 'merchant', None)

        if request.parent_site:
            set_thread_variable('parent_site', request.parent_site.pk)
        elif request.merchant:
            set_thread_variable('merchant', request.merchant.pk)

        response = self.get_response(request)
        return response

    def load_allowed_hosts(self):
        cached_domains = cache.get('allowed_domains_cache')

        if cached_domains is None:
            site_domains = Site.objects.values_list('domain', flat=True)
            cached_domains = list(set(site_domains) | set(settings.ALLOWED_HOSTS))
            cache.set('allowed_domains_cache', cached_domains, timeout=3600)
        settings.ALLOWED_HOSTS = cached_domains
