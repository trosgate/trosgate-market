from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Freelancer, FreelancerAccount
from account. models import Customer
from payments.models import PaymentAccount
# from teams.models import Package, Team, Invitation
# from django.utils.text import slugify


# @receiver(post_save, sender=Customer)
# def create_freelancer_profile(sender, instance, created, **kwargs):
#     '''
#     Create a freelancer profile ..
#     For user who signup as freelancer
#     '''
#     if created:
#         if instance.user_type == Customer.FREELANCER:
#             # Freelancer.objects.get_or_create(user=instance)[0]          
#             FreelancerAccount.objects.create(user=instance, merchant_id=instance.active_merchant_id)[0]
#             PaymentAccount.objects.create(user=instance, merchant_id=instance.active_merchant_id)[0]
            
















