import os
from .models import GatewaySetting
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(post_save, sender=GatewaySetting)
def enforce_default_setting(sender, instance, created, **kwargs):
    '''
    This function ensures that, Balance remains the default,
    We can use sender.objects or modelname.objects
    for readability, modelname is preferred
    '''
    GatewaySetting.objects.filter(default=True).update(default=False)
    GatewaySetting.objects.filter(name='balance').update(default=True, subscription=False)

