from .models import Notification
from general_settings.backends import get_from_email
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
# from general_settings.utilities import get_mailer
from django.template.loader import render_to_string


def create_notification(request, receiver, notification_type, slug):
    Notification.objects.create(receiver=receiver, notification_type=notification_type, sender=request.user, slug=slug)


def send_test_mail(to_email):
    from_email = get_from_email()
    subject = 'Activate your Team'
    text_content = f'Invitation to Gladiators.'
    html_content = render_to_string('teams/new_team_email.html', {
        'team': 'Team',
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

__all__ = ['send_new_test_mail_two']




























