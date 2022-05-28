from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from . models import Client, ClientAccount
from account.models import Customer
from transactions.models import SalesReporting, Purchase

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == Customer.CLIENT:
        client = Client.objects.create(user=instance)
        client.save()

        client_account = ClientAccount.objects.create(user=instance)
        client_account.save()


@receiver(post_save, sender=SalesReporting)
def create_employee_after_successful_checkout(sender, instance, created, **kwargs):
    if created and instance.purchase.status == Purchase.SUCCESS:
        employer = Client.objects.get(user=instance.client)

        if employer.employees.filter(id=instance.team.created_by.id).exists():
            pass
            
        else:
            employer.employees.add(instance.team.created_by.id)
            employer.save()

       