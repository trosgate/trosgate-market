import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Update domains.map file with current domains stored in the Sites Framework'

    def handle(self, *args, **options):
        # Get all active merchant sites
        merchant_sites = Site.objects.filter(domain__isnull=False)

        # Generate the new domains.map file content
        domains_map = ''
        for site in merchant_sites:
            domains_map += f"{site.domain} {site.merchant.upstream_server};\n"
            domains_map += f"*.{site.domain} {site.merchant.upstream_server};\n"

        # Write the new domains.map file
        with open(settings.NGINX_DOMAINS_MAP_FILE, 'w') as f:
            f.write(domains_map)

        # Restart Nginx to apply the changes
        os.system('sudo systemctl restart nginx')
