import subprocess
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings



class Command(BaseCommand):
    help = 'Request SSL certificates using Certbot'

    def handle(self, *args, **options):
        # Get all the sites from the Django Sites framework
        sites = Site.objects.all()

        for site in sites:
            # Prepare the command to run Certbot
            command = [
                'certbot',            # Certbot executable
                'certonly',           # Request a certificate
                '--webroot',          # Use webroot plugin
                '--webroot-path',     # '/webapps/trosgate/trosgate_env/trosgate-marketplace',
                os.path.join(settings.BASE_DIR, '/extras'),  # os.path.join(settings.BASE_DIR, '/extras')
                '-d',                 # Specify the domain
                site.domain            # Change this to the domain you want to request a certificate for
            ]

            try:
                # Run Certbot command
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f"Certbot command failed: {e}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Certificate obtained successfully for {site.domain}"))
