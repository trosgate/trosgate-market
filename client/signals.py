from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from . models import Client, ClientAccount
from account.models import Customer
from transactions.models import Purchase, ApplicationSale, ProposalSale, ContractSale


@receiver(post_save, sender=Customer)
def create_client_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == Customer.CLIENT:
        client = Client.objects.create(user=instance)
        client.save()

        client_account = ClientAccount.objects.create(user=instance)
        client_account.save()


@receiver(post_save, sender=ProposalSale)
def create_employee_after_successful_checkout(sender, instance, created, **kwargs):
    if instance.purchase.status == Purchase.SUCCESS:
        client = Client.objects.get(user=instance.purchase.client)

        if client.employees.filter(id=instance.team.created_by.id).exists():
            pass
            
        else:
            client.employees.add(instance.team.created_by.id)
            client.save()

       