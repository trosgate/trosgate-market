import os
from django.core.management import call_command
from celery import shared_task
from django.contrib.sites.models import Site


@shared_task()
def sync_domains():
    # Get all the site objects from the database
    sites = Site.objects.all()

    # Read the current contents of the domains.map file
    with open("/etc/nginx/domains.map", "r") as f:
        current_map = f.read()

    # Create a new map with the domains from the database
    new_map = ''
    for site in sites:
        new_map += f"{site.domain} {site.domain};\n"

    # Update the file if the new map is different
    if new_map != current_map:
        with open("/etc/nginx/domains.map", "w") as f:
            f.write(new_map)
        os.system("nginx -s reload")

        return 'Domains map file updated.'
    else:
        return 'No changes to domains map file.'
    








