from django.shortcuts import get_object_or_404
from twisted.internet.protocol import Protocol
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from account.models import Customer
from general_settings.backends import get_from_email


#
# Utility function for sending envites to team

def send_new_test_mail(to_email):
    from_email = get_from_email()
    subject = 'This is a test Email'
    message = 'This is a test Email to confirm that my email setup is fine'
    recipient_list = [to_email]
    html_message ='<h1> This is a test Email to confirm that my email setup is fine </h1>'

    send_mail(subject, message, from_email, recipient_list)

__all__ = ['send_new_test_mail']



def send_new_team_email(to_email, team):
    from_email = get_from_email()
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
    from_email = get_from_email()
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
    from_email = get_from_email()
    subject = 'Invitation accepted'
    text_content = 'Your invitation was accepted'
    context={
        'team': team, 
        'invitation': invitation
    }
    html_content = render_to_string('teams/accept_invitation_email.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
