from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import InternalContract, Contract
from account. models import Customer
from payments.models import PaymentAccount


@receiver(post_save, sender=InternalContract)
def create_internal_contract_reference(sender, instance, created, **kwargs):
    if created and instance.reference == '':
        ref = f'{instance.pk}'.zfill(8)
        instance.reference = f'Ex{instance.team.id}{instance.created_by.id}{ref}'
        instance.save()


@receiver(post_save, sender=Contract)
def create_external_contract_reference(sender, instance, created, **kwargs):
    if created and instance.reference == '':
        ref = f'{instance.pk}'.zfill(8)
        instance.reference = f'Ex{instance.team.id}{instance.created_by.id}{ref}'
        instance.save()
    












































