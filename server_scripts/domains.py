# Import the necessary libraries
import os
import django
from django.contrib.sites.models import Site


# A DIRECTORY CALLED domains MUST BE CREATED IN /etc/nginx/

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# Get all the site objects from the database
sites = Site.objects.all()

# Loop through the sites and write the domain mapping to a separate file
for site in sites:
    filename = f"/etc/nginx/domains/{site.domain}"
    with open(filename, "w") as f:
        f.write(f"{site.domain} {site.domain};\n")

# Open the domains.map file for writing
with open("/etc/nginx/domains.map", "w") as f:
    # Include all the domain files in the map block
    f.write("map $http_host $site {\n")
    f.write("    default default_site;\n")
    for site in sites:
        filename = f"/etc/nginx/domains/{site.domain}"
        f.write(f"    include {filename};\n")
    f.write("}\n")

# Reload Nginx configuration to apply changes
os.system("nginx -s reload")
