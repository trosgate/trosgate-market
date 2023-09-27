#
# Helper functions for sending team invitation

#
# Import from django
from twisted.internet.protocol import Protocol
from django.conf import settings
from account.models import Customer
from general_settings.backends import get_website_email
import uuid
#
# Import from python

from random import choice
from string import ascii_letters, digits
from django.utils import timezone
from datetime import timedelta


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# This will get the domain name we are on
def get_host_domain(request):
    return request.get_host().split(':')[0].lower()

#
# This will estimate subscription expiry by 30 days interval
def get_expiration():
    return (timezone.now() + timedelta(days = 30))

# This will get the domain name we are on

def get_host_domain(request):
    return request.get_host().split(':')[0].lower()

# Try to get the value from the settings module
SIZE = getattr(settings, "MAXIMUM_INVITE_SIZE", 6)

GENERATED_CHARS = ascii_letters + digits

def create_random_code(chars=GENERATED_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join([choice(chars) for _ in range(SIZE)])
    
#
def generate_unique_reference(model, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        # Generate a random UUID and convert it to a human-readable string
        reference = str(uuid.uuid4()).replace('-', '')[:8].upper()

        # Check if the generated reference is unique for the given model
        if not model.objects.filter(reference=reference).exists():
            return reference

        attempts += 1

    raise ValueError("Failed to create unique reference")