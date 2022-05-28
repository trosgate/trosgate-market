from django.conf import settings
from django.contrib import messages
from . models import WebsiteSetting
import requests

try:
    website = WebsiteSetting.objects.get(pk=1)
    secret_keys = website.secret_key
except:
    pass

def confirm_recaptcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret':secret_keys,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return function(request, *args, **kwargs)
    return wrap
