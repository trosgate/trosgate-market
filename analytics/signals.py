from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import F
from analytics.models import ProjectStatus
from projects . models import Project



@receiver(pre_save, sender=Project)
def create_project_status_stats(sender, instance, **kwargs):
    
    instance.active = ProjectStatus.objects.all().update(active=F('active') + Project.objects.all().filter(status = Project.ACTIVE).count())
    instance.review = ProjectStatus.objects.all().update(review=F('review') + Project.objects.all().filter(status = Project.REVIEW).count())
    instance.ongoing = ProjectStatus.objects.all().update(ongoing=F('ongoing') + Project.objects.all().filter(status = Project.ONGOING).count())
    instance.archived = ProjectStatus.objects.all().update(archived=F('archived') + Project.objects.all().filter(status = Project.ARCHIVED).count())
       
   

























