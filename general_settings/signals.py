from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from . models import PaymentGateway, Currency



@receiver(post_save, sender=PaymentGateway)
def create_or_only_one_default_gateway(sender, instance, created, **kwargs):
    PaymentGateway.objects.filter(status=True, default=True).update(default=False)
    PaymentGateway.objects.filter(status=True, id=instance.id).update(default=True)


@receiver(post_save, sender=Currency)
def create_or_only_one_default_currency(sender, instance, created, **kwargs):
    Currency.objects.filter(supported=True, default=True).update(default=False)
    Currency.objects.filter(supported=True, id=instance.id).update(default=True)















