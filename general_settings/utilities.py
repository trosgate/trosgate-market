from . models import WebsiteSetting
from django.conf import settings

def certificate():
    try:
        return WebsiteSetting.objects.get(pk=1).protocol
    except:
        return f'https'

def get_protocol():
    if certificate() == 'https://':
        return settings.USE_HTTPS
    else:
        return settings.USE_HTTP