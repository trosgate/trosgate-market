from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Customer, TwoFactorAuth


@receiver(post_save, sender=Customer)
def generate_TwoFactorAuth_code(sender, instance, created, **kwargs):

    if created:
        TwoFactorAuth.objects.create(user=instance)
        
        