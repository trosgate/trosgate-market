#
#Helper functions for sending team invitation

#
# Import from django
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.shortcuts import get_object_or_404
from twisted.internet.protocol import Protocol
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from general_settings.models import WebsiteSetting
from general_settings.utilities import get_protocol
from general_settings.backends import get_from_email
import random


# Twilio messaging
from twilio.rest import Client 
 
account_sid = 'AC70fb8218590a0dd00ed73988e04faed7' 
auth_token = '[38f735993c1afe7db44128d1a99bfff5]' 
client = Client(account_sid, auth_token) 

def send_verification_sms(user, pass_code, receiver_number):
    try:
        message = client.messages.create(
        body=f'Hi {user}, your login verification code is: {pass_code}',
        from_ = '+233557541875', 
        to=f'{receiver_number}'
    )
        print(message.sid)
        return message
    except:
        print('No communication with twilio to send SMS') 


try:
    website = WebsiteSetting.objects.get(pk=1)
    website_logo = website.site_logo_tag
except:
    pass



def auth_code():
    number_list = [x for x in range(10)]
    code_list = []

    for i in range(6):
        number = random.choice(number_list)
        code_list.append(number)
    passcode = "".join(str(code) for code in code_list)
    print('passcode: ',passcode)
    return passcode


#
# Utility function for sending signup mail
def new_user_registration(domain, user, to_email):
    from_email = get_from_email()
    # current_site = get_current_site(request)
    subject = 'Activate your Account'
    subtitle = f'Welcome to {website.site_name}'
    text_content = f'Welcome to {website.site_name}.'
    message = "You're almost ready to get started. Please click on the button below to verify your email address and enjoy exclusive cleaning services with us!"
    html_content = render_to_string('account/registration/register_activation_email.html', {
        # 'domain': current_site.domain,
        'website_email': from_email,
        'website_name': website.site_name,
        'domain': domain,
        'protocol': get_protocol(),
        'website_logo': website_logo,
        'user': user,
        'website': website,
        'subtitle': subtitle,
        'subject': subject,
        'message': message,
        # 'domain': current_site.domain,
        'acceptation_url': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),        
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

























