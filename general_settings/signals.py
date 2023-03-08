from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Currency


@receiver(post_save, sender=Currency)
def create_or_only_one_default_currency(sender, instance, created, **kwargs):
    if instance.id and instance.default == True:
        Currency.objects.filter(default=True).update(default=False)
        Currency.objects.filter(id=instance.id).update(supported=True, default=True)

    if Currency.objects.count() and Currency.objects.filter(default=True).count() == 0:
        currency = Currency.objects.last()
        currency.supported=True
        currency.default=True
        currency.save()















