from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from . models import Freelancer, FreelancerAccount
from account. models import Customer
from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale, SalesReporting, SubscriptionItem


@receiver(post_save, sender=Customer)
def create_freelancer_profile(sender, instance, created, **kwargs):
    '''
    Create a freelancer profile ..
    For user who signup as freelancer
    '''
    if created and instance.user_type == Customer.FREELANCER:
        freelancer = Freelancer.objects.create(user=instance)
        freelancer.save()
    
        freelancer_account = FreelancerAccount.objects.create(user=instance)
        freelancer_account.save()


@receiver(post_save, sender=Customer)
def create_new_admin_type(sender, instance, created, **kwargs):
    '''
    Create a freelancer profile ..
    For user who signup as freelancer
    '''
    if created and not (instance.user_type == Customer.FREELANCER  or instance.user_type == Customer.CLIENT):
        Customer.objects.filter(id=instance.id).update(user_type = Customer.ADMIN)


@receiver(post_save, sender=Purchase)
def mark_paid_and_credit_pending_balance(sender, instance, created, **kwargs):
    founder = ''
    freelancer = ''
    earning = ''
    print('initial run')
    if instance.category == 'proposal' and instance.status == 'success':

        for proposal in ProposalSale.objects.filter(purchase__id=instance.id):
            founder = proposal.team.created_by.id
            # earning = proposal.total_earning
            print('inside run')

            freelancer = Freelancer.active.get(user=founder)
            freelancer.pending_balance += int(124)
            freelancer.save()
            print('final run')





















































