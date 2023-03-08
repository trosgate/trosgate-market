# Import the necessary libraries
import os
import django
from django.contrib.sites.models import Site


# A FILE CALLED domains.map MUST BE CREATED IN /etc/nginx/

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# Get all the site objects from the database
sites = Site.objects.all()

# Open the domains.map file for writing
with open("/etc/nginx/domains.map", "w") as f:
    # Loop through the sites and write the domain mapping to the file
    for site in sites:
        f.write(f"{site.domain} {site.domain};\n")

# Reload Nginx configuration to apply changes
os.system("nginx -s reload")
