from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Freelancer, FreelancerAccount
from account. models import Customer




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


















































