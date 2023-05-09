# Import Python packages

import django
import os
import sys
import shutil
import subprocess

# Init Django

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trosgate.settings")
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseBadRequest


def generate_ssl_certficate(domain):

    # Check if the domain already has an SSL certificate by looking for the certificate files in the /etc/letsencrypt/live directory
    cert_dir = os.path.join('/etc/letsencrypt/live', domain)
    cert_file = os.path.join(cert_dir, 'cert.pem')
    key_file = os.path.join(cert_dir, 'privkey.pem')
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        # If the certificate files already exist, do nothing
        return HttpResponse(f"{domain} already has an SSL certificate.")
        
    # Generate an SSL certificate using Certbot
    certbot_args = [
        'certonly', 
        '--webroot', 
        '-w', settings.WEBROOT_PATH, 
        '-d', domain, 
        '--non-interactive',
        '--agree-tos', 
        '--email', 'admin@example.com'
    ]
    try:
        subprocess.run(['certbot'] + certbot_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        return HttpResponseBadRequest(f"Failed to generate SSL certificate: {e.stderr}")


    # If the certificate was successfully generated, save the domain and keyfile path in the database
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        # Read the contents of the keyfile and save it to the database
        try:
            with open(key_file, 'rb') as f:
                keyfile_data = f.read()
        except IOError:
            return HttpResponseBadRequest("Failed to read keyfile.")

        # Save the domain and keyfile data to the database here...
        return HttpResponse(f"{domain} SSL certificate generated and saved.")
    else:
        # If the certificate files were not generated, return an error
        return HttpResponseBadRequest("Failed to generate SSL certificate.")


