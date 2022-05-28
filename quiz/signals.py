from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from . models import Quizes


@receiver(post_save, sender=Quizes)
def enforce_quiz_max_question(sender, instance, created, **kwargs):
    if created or not created and instance.questions.count() < 5:
        Quizes.objects.filter(id=instance.id).update(is_published=False)        

    
   

























