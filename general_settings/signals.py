from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from . models import PaymentGateway, WebsiteSetting, TestEmail, Currency
from django.contrib.sites.shortcuts import get_current_site
from notification.utilities import send_new_test_mail, send_new_test_mail_two
# from teams.utilities import send_new_team_email


@receiver(post_save, sender=PaymentGateway)
def create_or_only_one_default_gateway(sender, instance, created, **kwargs):
    PaymentGateway.objects.filter(status=True, default=True).update(default=False)
    PaymentGateway.objects.filter(status=True, id=instance.id).update(default=True)


@receiver(post_save, sender=Currency)
def create_or_only_one_default_currency(sender, instance, created, **kwargs):
    Currency.objects.filter(supported=True, default=True).update(default=False)
    Currency.objects.filter(supported=True, id=instance.id).update(default=True)


#This is for Test Email sending
@receiver(post_save, sender=TestEmail)
def send_test_mail(sender, instance, created, **kwargs): 
    try:
        send_new_test_mail_two(instance.test_email)
        print('mail sent to:', instance.test_email)
    except:
        print('mail not sent to:', instance.test_email)

__all__ = ['send_test_mail']













