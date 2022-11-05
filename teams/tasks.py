from account.models import Customer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from celery import shared_task
from general_settings.backends import get_from_email


#Send a mail via celery
@shared_task(bind=True)
def email_all_users(self):
    freelancers = Customer.objects.filter(is_active = True)
    for freelancer in freelancers:
       # timezone.localtime(freelancer.date_time) #Only required if users must see message in their localtime
        from_email = get_from_email()
        to_email = freelancer.email
        to_username = freelancer.short_name

        text_content = f"Test Email to {to_username}"
        html_content = render_to_string('notification/test_email.html', {
            'website_email': from_email,
            'text_content': text_content
        })
        msg = EmailMultiAlternatives(to_username, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
  
    return 'Mail Sent'
