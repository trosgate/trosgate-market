from account.models import Customer
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from celery import shared_task

#Send a mail via celery
@shared_task(bind=True)
def email_all_users(self):
    freelancers = Customer.objects.filter(is_active = True)
    for freelancer in freelancers:
       # timezone.localtime(freelancer.date_time) #Only required if users must see message in their localtime
        from_email = settings.DEFAULT_EMAIL_FROM
        to_email = freelancer.email
        to_username = freelancer.short_name
        acceptation_url = settings.ACCEPTATION_URL

        subject = 'Activate your Account'
        text_content = 'Welcome to Trosgate'
        html_content = render_to_string('teams/admin_email_freelancer.html', {
            'email': to_email,
            'username': to_username,
            'acceptation_url': acceptation_url,
        })

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
  
    return 'Mail Sent'
