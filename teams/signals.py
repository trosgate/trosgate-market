from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from teams.models import  Package


@receiver(post_save, sender=Package)
def maintain_state_of_the_two_packages(sender, instance, created, **kwargs):
    Package.objects.filter(id=1, type='Basic').update(max_member_per_team=1, price=0, is_default=True)        
    Package.objects.filter(id=2, type='Team').update(is_default=False)        
