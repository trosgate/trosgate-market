from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import HelpDesk
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=HelpDesk)
def help_desk_default_setting(sender, instance, created, **kwargs):
    '''
    A good time to create assigner to the proposal
    '''
    if created or not created:
        HelpDesk.objects.filter(published=True).update(published=False)
        HelpDesk.objects.filter(pk=instance.id).update(published=True)
        

