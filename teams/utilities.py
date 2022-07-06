#
# Helper functions for sending team invitation

#
# Import from django
from django.shortcuts import get_object_or_404
from twisted.internet.protocol import Protocol
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from account.models import Customer
from general_settings.backends import get_website_email

#
# Import from python

from random import choice
from string import ascii_letters, digits
#
# This will get the domain name we are on

def get_host_domain(request):
    return request.get_host().split(':')[0].lower()

# Try to get the value from the settings module
SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 50)

GENERATED_CHARS = ascii_letters + digits


def create_random_code(chars=GENERATED_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join([choice(chars) for _ in range(SIZE)])
    
#
# Try to avoid the possible chance of repeated code with function below
def create_shortened_url(model_instance):
    random_code = create_random_code()

    # This line help to avoid error when we make circular imports between models and this file- utilities
    model_class = model_instance.__class__

    if model_class.objects.filter(invite_url=random_code).exists():
        # Run the function again
        return create_shortened_url(model_instance)

    return random_code

