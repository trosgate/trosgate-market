from django.db.models.signals import post_save
from django.dispatch import receiver
from general_settings.models import TestEmail
from notification.mailer import send_test_mail


#This is for Test Email sending
@receiver(post_save, sender=TestEmail)
def test_mail(sender, instance, created, **kwargs): 
    try:
        send_test_mail(instance.test_email)
    except:
        print('mail not sent to:', instance.test_email)






























