from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Client
from transactions.models import Purchase, ApplicationSale, ProposalSale, ContractSale


@receiver(post_save, sender=Purchase)
def add_founder_to_client_employees_after_checkout(sender, instance, created, **kwargs):
    client = Client.objects.get(user=instance.client)
    if instance.status == 'success' and instance.category == 'proposal':
        if ProposalSale.objects.filter(purchase=instance).exists():
            proposal = ProposalSale.objects.get(purchase=instance)
            if client.employees.filter(id=proposal.team.created_by.id).exists():
                pass
            else:
                client.employees.add(proposal.team.created_by.id)
                client.save()

    elif instance.status == 'success' and instance.category == 'project':
        if ApplicationSale.objects.filter(purchase=instance).exists():
            application = ApplicationSale.objects.get(purchase=instance)
            if client.employees.filter(id=application.team.created_by.id).exists():
                pass
            else:
                client.employees.add(application.team.created_by.id)
                client.save()
                
    elif instance.status == 'success' and instance.category == 'contract':
        if ContractSale.objects.filter(purchase=instance).exists():
            contract = ContractSale.objects.get(purchase=instance)
            if client.employees.filter(id=contract.team.created_by.id).exists():
                pass
            else:
                client.employees.add(contract.team.created_by.id)
                client.save()


# @receiver(post_save, sender=ProposalSale)
# def create_employee_after_proposal_checkout(sender, instance, created, **kwargs):
#     if instance.purchase.status == Purchase.SUCCESS:
#         client = Client.objects.get(user=instance.purchase.client)

#         if client.employees.filter(id__in=instance.team.created_by.id).exists():
#             pass
            
#         else:
#             client.employees.add(instance.team.created_by.id)
#             client.save()
