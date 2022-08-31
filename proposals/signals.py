from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from proposals.models import Proposal
from teams.models import Team, AssignMember
from django.utils.text import slugify
from datetime import datetime, timezone, timedelta
from django.utils.translation import gettext_lazy as _
import os

@receiver(pre_save, sender=Proposal)
def replace_old_thumbnail_with_new_one(sender, instance, **kwargs):
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        prev_thumbnail = sender.objects.get(pk=instance.pk).thumbnail
    except sender.DoesNotExist:
        return False
    
    thumbnail = instance.thumbnail
    if not prev_thumbnail == thumbnail:
        if os.path.isfile(prev_thumbnail.path):
            os.remove(prev_thumbnail.path)


@receiver(post_save, sender=Proposal)
def create_proposal_reference(sender, instance, created, **kwargs):
    if created and instance.reference == '':
        ref = f'{instance.pk}'.zfill(8)
        instance.reference = f'P{instance.team.id}{instance.created_by.id}{ref}'
        instance.save()


@receiver(post_save, sender=Proposal)
def create_and_assign_proposal_task(sender, instance, created, **kwargs):
    '''
    A good time to create assigner to the proposal
    '''
    if created:
        assign_task = AssignMember.objects.create(
            team=instance.team, 
            proposal=instance, 
            status=AssignMember.TODO, 
            assignor = instance.team.created_by,
            assignee=instance.created_by,
            is_assigned=False
        )
        assign_task.save()


@receiver(post_save, sender=Proposal)
def update_assign_proposal_task(sender, instance, created, **kwargs):
    if not created and instance.status == Proposal.ACTIVE:
        AssignMember.objects.filter(proposal=instance).update(is_assigned=True)
