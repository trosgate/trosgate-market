#
#Helper functions forgenerating 2FA Code
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps

import random


def auth_code():
    number_list = [x for x in range(10)]
    code_list = []

    for i in range(6):
        number = random.choice(number_list)
        code_list.append(number)
    passcode = "".join(str(code) for code in code_list)

    return passcode


def load_allowed_hosts():
    domains = set(settings.ALLOWED_HOSTS)
    Site = apps.get_model('sites', 'Site')
    sites = Site.objects.all()
    for site in sites:
        domains.add(site.domain)
    return list(domains)

















