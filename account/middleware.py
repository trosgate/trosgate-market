import re
import subprocess
import os
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from account.models import Customer, Merchant
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout


class DynamicHostMiddleware:
    '''
        To update the URLs dynamically based on the requested domain, 
        we can create a  
        Here's an example of how the middleware might look:

        This middleware first checks if the requested domain is in the database 
        by querying the Site model. If a matching site is found, 
        this middleware intercepts the request, checks if status of merchant is activated 
        and updates the domain portion of the requested URL if the domain is in the database.
        the middleware sets the request.site attribute to the Site object 
        and updates the urlconf and SITE_ID settings to match the site.

        Finally, it updates the requested URL with the correct domain 
        using the HTTP_HOST key in the request.META dictionary.

        With this middleware in place, URLs generated by Django's built-in URL routing functions
        should automatically use the correct domain based on the requested URL. 
        For example, if a user visits http://my-merchant-business.mysite.com/dashboard/, 
        the URL generated by reverse('dashboard') would be 
        http://my-merchant-business.mysite.com/dashboard/.   

        Note that with this solution, we are using the sites framework to store the domain and 
        site ID information, and we are querying the database to retrieve 
        this information at runtime. This avoids modifying the settings module directly 
        and is a better approach in terms of maintainability and scalability.    
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.get_host().lower().split(':')[0]
        if domain.startswith('www.'):
            domain = domain[4:]
        
        try:
            # Look up the Site object for the requested domain
            site = Site.objects.get(domain=domain)
            
            # Set the SITE_ID header to the ID of the Site object          
            request.META['SITE_ID'] = site.id # or settings.SITE_ID = site.id
            
            # Call the next middleware or view function
            response = self.get_response(request)

        except Site.DoesNotExist:
            return HttpResponseForbidden()
      
        # Check if SSL certificate exists for the domain
        if os.path.exists(f"/etc/letsencrypt/live/{site.domain}/fullchain.pem"):
            ssl_certificate = f"/etc/letsencrypt/live/{site.domain}/fullchain.pem"
            ssl_certificate_key = f"/etc/letsencrypt/live/{site.domain}/privkey.pem"
        
        else:
            # Generate SSL certificate using Certbot
            cmd = f"certbot certonly --nginx -d {site.domain} -n --agree-tos --email admin@{site.domain}"
            subprocess.run(cmd.split())

            ssl_certificate = f"/etc/letsencrypt/live/{site.domain}/fullchain.pem"
            ssl_certificate_key = f"/etc/letsencrypt/live/{site.domain}/privkey.pem"

        # Configure the upstream server based on the value of the HTTP_UPSTREAM header
        upstream = request.META.get('HTTP_UPSTREAM', 'error')

        # Set an atribute to differentiate parent site instance from all other merchants
        if site.id == 1:
            request.parent = site
        else:
            request.parent = None

        # Configure the SSL block for the domain
        ssl_block = f"""
            ssl_certificate {ssl_certificate};
            ssl_certificate_key {ssl_certificate_key};
        """

        # Configure the server block for the domain
        server_block = f"""
            server {{
                listen 443 ssl;

                # Set the upstream server based on the value of the HTTP_UPSTREAM header
                # if in test environment, proxy_pass will listen on port 8000;
                # if in live environment, proxy_pass will listen on port 80;

                location / {{
                    proxy_pass http://{upstream}:80;
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Scheme $scheme;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }}

                # Configure SSL for the domain
                {ssl_block}
            }}
        """

        # Configure the default server block for unknown domains
        default_server_block = f"""
            server {{
                listen 443 ssl;
                server_name _;

                # Return a 403 Forbidden response for unknown domains
                return 403;

                # SSL configuration goes here
                {ssl_block}
            }}
        """

        return response, server_block, default_server_block, upstream

        # Call the next middleware or view function
        # response = self.get_response(request)

        # redirect_url = reverse('/')
        # return HttpResponseRedirect(redirect_url)

        # return response


class MerchantGateMiddleware:
    """
    Check that an account is in a valid status to permit access.
    Inactive accounts will be redirected to a plan selection page
    unless the URL is on an allowed list of routes.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_list_patterns = [
            re.compile(fr"^{allowed}$") for allowed in settings.MERCHANT_GATE_ALLOW_LIST
        ]

    def __call__(self, request):
        request.merchant = None
        if request.user.is_authenticated and request.user.user_type == 'merchant':

            sitee = Site.objects.get_current()
            request.merchant = Merchant.curr_merchant.first()
            print('request.sitee :', sitee, request.merchant.site)
            gate_url = reverse("account:dashboard") # subscriptions:complete
            if (
                request.merchant.type in Merchant.ACTIVE_TYPES
                or request.path_info == gate_url # MEANING THEY ARE WHERE THEY SHOULD BE CHECKING OUT
                or self.is_granted_passage(request.path_info)
            ):
                return self.get_response(request)

            return HttpResponseRedirect(gate_url)
        return self.get_response(request)

    def is_granted_passage(self, path):
        """Check if the request is allowed against the allow list."""
        return any(pattern.match(path) for pattern in self.allow_list_patterns)
