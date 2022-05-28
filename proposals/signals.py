from django.db.models.signals import post_save
from django.dispatch import receiver
from proposals.models import Proposal
from teams.models import Team, AssignMember
from django.utils.text import slugify
from datetime import datetime, timezone, timedelta
from django.utils.translation import gettext_lazy as _


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
def create_and_assign_proposal_task(sender, instance, created, **kwargs):
    if not created and instance.status == Proposal.ACTIVE:
        AssignMember.objects.filter(proposal=instance).update(is_assigned=True)
