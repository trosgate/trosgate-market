from django.core.mail.backends.smtp import EmailBackend
from . models import Mailer


def get_website_email():
    try:
        return Mailer.objects.get(id=1).from_email 
    except:
        return None

def get_email_hosting_server():
    try:
        return Mailer.objects.get(id=1).email_hosting_server 
    except:
        return None

def get_email_hosting_server_password():
    try:
        return Mailer.objects.get(id=1).email_hosting_server_password 
    except:
        return None

def get_email_hosting_server_port():
    try:
        return Mailer.objects.get(id=1).email_hosting_server_port 
    except:
        return None

def get_email_use_tls_certificate():
    try:
        return Mailer.objects.get(id=1).email_use_tls 
    except:
        return None

def get_email_use_ssl_certificate():
    try:
        return Mailer.objects.get(id=1).email_use_ssl 
    except:
        return None

def get_from_email():
    try:
        return Mailer.objects.get(id=1).get_from_email 
    except:
        return None

def get_email_fail_silently():
    try:
        return Mailer.objects.get(id=1).email_fail_silently 
    except:
        return None

def get_email_timeout():
    try:
        return Mailer.objects.get(id=1).email_timeout 
    except:
        return None

def get_email_hosting_username():
    try:
        return Mailer.objects.get(id=1).email_hosting_username 
    except:
        return None


class MailerBackend(EmailBackend):
    def __init__(self, host=None, port=None, username=None, password=None, use_tls=None, fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None, ssl_certfile=None, **kwargs):

        super(MailerBackend, self).__init__(
            host= get_email_hosting_server() if host is None else host, 
            port= get_email_hosting_server_port() if port is None else port, 
            username= get_email_hosting_username() if username is None else username,  
            password = get_email_hosting_server_password() if password is None else password, 
            use_tls= get_email_use_tls_certificate() if use_tls is None else use_tls, 
            fail_silently= get_email_fail_silently() if fail_silently is None else fail_silently,
            use_ssl= get_email_use_ssl_certificate() if use_ssl is None else use_ssl, 
            timeout= get_email_timeout() if timeout is None else timeout, 
            **kwargs)

__all__ = ['MailerBackend']




# from django.core import mail
# from general_settings.utilities import (
#     get_email_hosting_server,
#     get_email_hosting_server_password,
#     get_email_hosting_server_port,
#     get_email_use_tls_certificate,
#     get_email_use_ssl_certificate,
#     get_email_hosting_server_email,
#     get_email_fail_silently
# )

# connection = mail.get_connection(
#     email_hosting_server= get_email_hosting_server(), 
#     email_hosting_server_password= get_email_hosting_server_password(), 
#     email_hosting_server_port= get_email_hosting_server_port(),
#     email_use_tls= get_email_use_tls_certificate(),
#     email_use_ssl= get_email_use_ssl_certificate(),
#     email_hosting_server_email= get_email_hosting_server_email(),
#     email_fail_silently= get_email_fail_silently(),
# )










