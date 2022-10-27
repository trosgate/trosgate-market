from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Freelancer, FreelancerAccount
from account. models import Customer
from payments.models import PaymentAccount


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

        freelancer_payment_account = PaymentAccount.objects.create(user=instance)
        freelancer_payment_account.save()

















































