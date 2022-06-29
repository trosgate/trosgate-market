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

#
# Utility function for sending envites to team




def send_new_team_email(to_email, team):
    from_email = get_website_email()
    acceptation_url = settings.WEBSITE_URL
    subject = 'Activate your Team'
    text_content = f'Invitation to {team.title}.'
    html_content = render_to_string('teams/new_team_email.html', {
        'protocol': Protocol,
        'team': team,
        'acceptation_url': acceptation_url,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Utility function for sending envites to team
def send_invitation_email(to_email, code, team):
    from_email = get_website_email()
    acceptation_url = settings.WEBSITE_URL
    subject = 'Invitation to Team'
    text_content = f'Invitation to {team.title}. Your code is: %s' % code
    html_content = render_to_string('teams/email_invitation.html', {
        'protocol': Protocol,
        'team': team,
        'code': code,
        'acceptation_url': acceptation_url,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#
# Utility function for notifying team founder when envites accept your invitation


def send_invitation_accepted_mail(team, invitation):
    from_email = settings.DEFAULT_EMAIL_FROM
    subject = 'Invitation accepted'
    text_content = 'Your invitation was accepted'
    html_content = render_to_string(
        'teams/accept_invitation_email.html', {'team': team, 'invitation': invitation})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [
                                 team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
