from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Customer, TwoFactorAuth


@receiver(post_save, sender=Customer)
def generate_TwoFactorAuth_code(sender, instance, created, **kwargs):

    if created:
        TwoFactorAuth.objects.create(user=instance)
        

# @receiver(post_save, sender=Customer)
# def create_new_admin_type(sender, instance, created, **kwargs):
#     '''
#     Enforce Admin status as long as the Superuser is the one adding user
#     '''
#     if created and not (instance.user_type == Customer.FREELANCER  or instance.user_type == Customer.CLIENT):
#         Customer.objects.filter(id=instance.id).update(is_active=True, is_staff=True, is_assistant=True, user_type = Customer.ADMIN)


